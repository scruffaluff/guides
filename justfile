# Just configuration file for running commands.
#
# For more information, visit https://just.systems.

set script-interpreter := ["nu"]
set shell := ["nu", "--commands"]
export PATH := if os() == "windows" {
  justfile_directory() / ".vendor/bin;" + env("PATH")
} else {
  justfile_directory() / ".vendor/bin:" + env("PATH")
}

# Build website.
[script]
build:
  uv build --out-dir build/dist
  deno run --allow-all npm:vitepress build .
  for note in (ls doc/note/*.md | get name) {
    let subpath = $note | path relative-to doc | path parse | $"($in.parent)/($in.stem)"
    let html = $"build/site/($subpath).html"
    uv run marimo --yes export html-wasm --output $html $note
  }
  rm --force --recursive build/site/files build/site/note/CLAUDE.md
  cp build/dist/note-*-py3-none-any.whl build/site/file/note-1.0.0-py3-none-any.whl

# Execute CI workflow commands.
ci: setup lint build

# Wrapper to Deno.
[no-exit-message]
@deno *args:
  deno {{args}}

# Launch website in developer mode.
dev *flags:
  deno run --allow-all npm:vitepress dev . {{flags}}

# Fix code formatting.
format +paths=".":
  deno run --allow-all npm:prettier --write {{paths}}
  uv run ruff format {{paths}}

# Run code analyses.
lint +paths=".":
  deno run --allow-all npm:prettier --check {{paths}}
  uv run ruff format --check {{paths}}
  uv run ruff check {{paths}}
  uv run ty check {{paths}}

# List all commands available in justfile.
[default]
list:
  just --list

# Wrapper to Nushell.
[no-exit-message]
@nu *args:
  nu {{args}}

# Serve built website.
serve *flags: build
  deno run --allow-all npm:vitepress serve . {{flags}}

# Install development dependencies.
[script]
setup: _setup
  if (which deno | is-empty) {
    print "Installing Deno."
    http get https://scruffaluff.github.io/picoware/install/deno.nu
    | nu -c $"($in | decode); main --preserve-env --dest .vendor/bin"
  }
  print $"Using (deno -V)."
  if (which uv | is-empty) {
    print "Installing Uv."
    http get https://scruffaluff.github.io/picoware/install/uv.nu
    | nu -c $"($in | decode); main --preserve-env --dest .vendor/bin"
  }
  print $"Using (uv --version)."
  print "Installing Python packages with Deno and Uv."
  if ($env.JUST_INIT? | is-empty) {
    deno install --frozen
    uv sync --locked
  } else {
    deno install
    uv sync
  }

[unix]
_setup:
  #!/usr/bin/env sh
  set -eu
  if [ ! -x "$(command -v nu)" ]; then
    echo 'Installing Nushell'.
    curl --fail --location --show-error \
      https://scruffaluff.github.io/picoware/install/nushell.sh | sh -s -- \
      --preserve-env --dest .vendor/bin
  fi
  echo "Using Nushell $(nu --version)."

[windows]
_setup:
  #!powershell.exe
  $ErrorActionPreference = 'Stop'
  $ProgressPreference = 'SilentlyContinue'
  $PSNativeCommandUseErrorActionPreference = $True
  if (-not (Get-Command -ErrorAction SilentlyContinue nu)) {
    Write-Output 'Installing Nushell.'
    $NushellScript = Invoke-WebRequest -UseBasicParsing -Uri `
      https://scruffaluff.github.io/picoware/install/nushell.ps1
    Invoke-Expression "& { $NushellScript } --preserve-env --dest .vendor/bin"
  }
  Write-Output "Using Nushell $(nu --version)."

# Wrapper to Uv.
[no-exit-message]
@uv *args:
  uv {{args}}
