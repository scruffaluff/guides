---
layout: page
title: Compression
---

<script setup>
import { onMounted, onUnmounted } from "vue";
onMounted(() => {
  document.body.style.overflowY = "hidden";
})
onUnmounted(() => {
  document.body.style.overflowY = "";
})
</script>

<iframe
  allow="microphone"
  allowfullscreen
  class="notebook"
  sandbox="allow-scripts allow-same-origin allow-downloads"
  src="/guides/nb/compress.html"
></iframe>
