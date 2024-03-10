<template>
  <div class="main-hub-list-viewer mx-xl-5">
    <div class="container-fluid">
      <div class="row hub-list-row">
        <div class="col-3">yo</div>
        <div class="col bg-dark d-flex flex-column">
          <h3 class="px-3 text-light mt-2" style="text-align: start">HUBS</h3>
          <div class="d-flex justify-content-start pb-3 border-bottom">
            <div class="input-group me-2">
              <input
                type="text"
                class="form-control filter"
                placeholder="Search for schedule"
              />
            </div>
            <button class="btn btn-primary">CREATE</button>
          </div>
          <div class="hub-list-container px-3">
            <div
              v-for="hub in hubList"
              class="text-light mb-2"
              :key="hub.HubID"
            >
              <div class="card">
                <div class="container">
                  <div class="row">
                    <div class="col-8">{{ hub.HubName }}</div>
                    <div class="col-4">HELLO</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import axios from "axios";
import { HubsList } from "@/modules/hubs/types";

const hubList = ref<HubsList[]>([]);

const setup = async () => {
  let data = await axios.get("http://localhost:5000/hub", {
    withCredentials: true,
  });

  hubList.value = data.data;
};

setup();
</script>

<style lang="scss">
.main-hub-list-viewer {
  display: flex;
  flex-grow: 1;
  background-color: rgb(53, 63, 98);
  min-height: 0;
}

.hub-list-row {
  height: 100%;
}

.hub-list-container {
  height: 100%;
  flex-grow: 1;
  overflow-y: scroll;
}

.main-hub-list-viewer > div {
  max-height: 100%;
}

div {
  min-height: 0;
  max-height: 100%;
}
</style>
