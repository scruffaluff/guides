<template>
  <p>The count is {{ count }}.</p>
  <button class="button" @click="count++">Increment</button>
</template>

<script setup>
import { ref } from "vue";

const count = ref(0);
</script>

<style scoped>
.button {
  color: green;
  font-weight: bold;
}
</style>
