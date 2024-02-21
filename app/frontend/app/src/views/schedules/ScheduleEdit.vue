<template>
  <div class="main mx-0 d-flex">
    <div class="header">
      <h2>Name of the schedule</h2>
    </div>
    <div class="container-fluid mx-0 px-0">
      <div class="row mx-0">
        <div class="col-8 p-3" style="max-height: 100">
          <trigger-block />
        </div>
        <div class="col-4 px-0">
          <block-menu />
        </div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import BlockMenu from "./BlockMenu.vue";
import BlockItem from "./BlockItem.vue";
import TriggerBlock from "./TriggerBlock.vue";
import BlockConditionals from "./BlockConditionals.vue";
</script>
<style>
.main {
  height: 100%;
  width: 100%;
  background-color: rgb(45, 50, 64);
  flex-direction: column;
}

.header {
  background-color: rgb(58, 64, 81);
  min-height: 4rem;
}

.container-fluid {
  height: 100%;
}

.row {
  height: 100%;
}

body {
  color: white;
}
</style>
