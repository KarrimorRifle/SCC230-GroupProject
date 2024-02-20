<template>
  <div id="editor" class="main p-3">
    <block-item :command-type="'IF'" />
  </div>
</template>
<script setup lang="ts">
import BlockItem from "./BlockItem.vue";
</script>
<style>
#editor {
  background-color: rgb(81, 90, 113);
  height: 100%;
}
</style>
