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
              class="text-light mt-2 mb-1"
              :key="hub.HubID"
            >
              <div class="card">
                <div class="row">
                  <div
                    class="col-xl-8 col-lg-7 col-md-6 col-4 border-end ps-4 d-flex justify-content-start align-items-center"
                  >
                    <b>
                      {{
                        hub.HubName.length > 25
                          ? hub.HubName.slice(0, 24) + "..."
                          : hub.HubName
                      }}
                    </b>
                  </div>
                  <div class="col-md-1 col-2 border-end mt-1">
                    <img
                      v-if="hub.PermissionLevel == 5"
                      src="@/assets/permissions/5.svg"
                      alt=""
                      style="max-width: 2rem"
                    />
                    <img
                      v-else-if="hub.PermissionLevel == 4"
                      src="@/assets/permissions/4.svg"
                      alt=""
                      style="max-width: 2rem"
                    />
                    <img
                      v-else-if="hub.PermissionLevel == 3"
                      src="@/assets/permissions/3.svg"
                      alt=""
                      style="max-width: 2rem"
                    />
                    <img
                      v-else-if="hub.PermissionLevel == 2"
                      src="@/assets/permissions/2.svg"
                      alt=""
                      style="max-width: 2rem"
                    />
                    <img
                      v-else-if="hub.PermissionLevel == 1"
                      src="@/assets/permissions/1.svg"
                      alt=""
                      style="max-width: 2rem"
                    />
                  </div>
                  <div class="col-xl-3 col-lg-4 col-md-5 col-6 py-1">
                    <a
                      class="btn btn-sm btn-secondary me-2"
                      v-if="hub.PermissionLevel == 5"
                      :href="`/hubs/${hub.HubID}`"
                    >
                      EDIT
                    </a>
                    <button
                      class="btn btn-sm btn-info me-2"
                      @click="console.log('VIEWING')"
                      v-if="hub.PermissionLevel >= 1"
                    >
                      VIEW
                    </button>
                    <button
                      class="btn btn-sm btn-danger mt-sm-0 mt-2"
                      @click="console.log('DELETING')"
                      v-if="hub.PermissionLevel == 5"
                    >
                      DELETE
                    </button>
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

  console.log(data.data);
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
