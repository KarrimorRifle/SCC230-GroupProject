<template>
  <div class="main-hub-viewer mx-xl-5 d-flex">
    <div class="container-fluid flex-grow-1">
      <div
        class="row hub-row px-0"
        style="min-height: 0; max-height: 100%; height: 100%"
      >
        <div class="col-3 text-start bg-dark px-0"></div>
        <div class="col-9 px-0">
          <div class="container-fluid text-light" v-if="hub">
            <div class="row d-flex justify-content-start mt-2">
              <h2 class="text-start ps-3">
                <b>HUB PAGE</b>
              </h2>
            </div>
            <div class="row">
              <div class="input-group">
                <div class="input-group-text">Name</div>
                <input type="text" class="form-control" v-model="hub.HubName" />
                <button
                  class="input-group-text btn btn-success"
                  @click="updateHubName()"
                >
                  Update Name
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import axios from "axios";
import { HubBase } from "@/modules/hubs/types";
import router from "@/router";

const hub = ref<HubBase>();

const setup = async () => {
  let hubID = router.currentRoute.value.params.id;
  let data = await axios.get(`http://localhost:5000/hub/${hubID}`, {
    withCredentials: true,
  });

  console.log(data.data);
  hub.value = data.data;
};

const updateHubName = () => {
  console.log("updating");
};
setup();
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
