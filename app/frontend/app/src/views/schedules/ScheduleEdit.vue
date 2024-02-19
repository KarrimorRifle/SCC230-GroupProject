<template>
  <div class="main mx-0 d-flex">
    <div class="header">
      <h2>Name of the schedule</h2>
    </div>
    <div class="container-fluid mx-0 px-0">
      <div class="row mx-0">
        <div class="col-9 px-0">hello</div>
        <div class="col-3 px-0">
          <block-editor />
        </div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import BlockEditor from "./BlockEditor.vue";
</script>
<style>
.main {
  height: 100%;
  width: 100%;
  background-color: rgb(35, 39, 49);
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
