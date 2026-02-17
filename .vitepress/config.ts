// VitePress documentation configuration file.
//
// This configuration uses the default VitePress theme, whose details can be
// found at https://vitepress.dev/reference/default-theme-config. For more
// information on VitePress configuration, visit
// https://vitepress.dev/reference/site-config.

import { fileURLToPath, URL } from "node:url";
import { defineConfig } from "vitepress";
import { VitePWA } from "vite-plugin-pwa";
import { generateSidebar } from "vitepress-sidebar";

export default defineConfig({
  base: "/guides/",
  description: "Personal collection of notes, tutorials, and workbooks.",
  // Head contents follow the progressive web apprequirements specified at
  // https://vite-pwa-org.netlify.app/guide/pwa-minimal-requirements.html.
  head: [
    ["link", { href: "/guides/apple-touch-icon.png", rel: "apple-touch-icon" }],
    ["link", { href: "/guides/favicon.ico", rel: "icon", sizes: "48x48" }],
    [
      "link",
      {
        href: "/guides/favicon.svg",
        rel: "icon",
        sizes: "any",
        type: "image/svg+xml",
      },
    ],
    ["link", { href: "/guides/site.webmanifest", rel: "manifest" }],
  ],
  lastUpdated: true,
  markdown: {
    math: true,
  },
  outDir: "build/site",
  srcDir: "doc",
  srcExclude: ["**/note/*.md"],
  themeConfig: {
    aside: false,
    nav: [
      { text: "Home", link: "/" },
      { text: "Audio", link: "/audio/" },
    ],
    search: {
      provider: "local",
    },
    sidebar: generateSidebar([
      {
        documentRootPath: "doc",
        resolvePath: "/audio/",
        scanStartPath: "audio",
        useTitleFromFileHeading: true,
      },
    ]),
    socialLinks: [
      { icon: "github", link: "https://github.com/scruffaluff/guides" },
    ],
  },
  title: "Guides",
  vite: {
    publicDir: "../data/public",
    plugins: [
      // @ts-expect-error Type error is incorrect.
      VitePWA({
        manifest: false,
        registerType: "autoUpdate",
      }),
    ],
    resolve: {
      alias: {
        "@": fileURLToPath(new URL("../src/vue", import.meta.url)),
      },
    },
  },
});
