<template>
  <div class="main-hub-viewer mx-xl-5">
    <div class="container-fluid">
      <div class="row hub-row">
        <div class="col-3 text-light">hi</div>
        <div class="col bg-dark d-flex flex-column">hello</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
console.log("HI");
</script>

<style lang="scss">
.main-hub-viewer {
  display: flex;
  flex-grow: 1;
  background-color: rgb(32, 38, 62);
  min-height: 0;
}

.main-hub-viewer > div {
  max-height: 100%;
}

div {
  min-height: 0;
  max-height: 100%;
}
</style>
