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
                placeholder="Search for Hub"
                v-model="searchValue"
              />
            </div>
            <button class="btn btn-outline-primary border-2 text-light">
              CREATE
            </button>
          </div>
          <div class="hub-list-container px-3">
            <div
              v-for="hub in filteredHubs"
              class="text-light mt-2 mb-1"
              :key="hub.HubID"
            >
              <div class="card border-0 hub-card">
                <div class="row">
                  <div
                    class="col-md-1 col-2 ps-4"
                    :class="{
                      'my-1': hub.PermissionLevel != 5,
                      'mt-2': hub.PermissionLevel == 5,
                    }"
                  >
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
                  <div
                    class="col ps-3 d-flex border-start justify-content-start align-items-center"
                  >
                    <a
                      :href="`/hubs/${hub.HubID}`"
                      style="text-decoration: none"
                      class="text-light"
                    >
                      <b>
                        {{
                          hub.HubName.length > 25
                            ? hub.HubName.slice(0, 24) + "..."
                            : hub.HubName
                        }}
                      </b>
                    </a>
                  </div>
                  <div
                    class="col-xxl-2 col-xl-3 col-lg-3 col-md-4 col-5 ps-2 py-2 border-start d-flex"
                    v-if="hub.PermissionLevel == 5"
                  >
                    <button
                      class="btn btn-sm btn-outline-secondary me-2 text-light border-2"
                      :href="`/hubs/${hub.HubID}`"
                    >
                      EDIT
                    </button>
                    <button
                      class="btn btn-sm btn-outline-danger mt-sm-0 mt-2 text-light border-2"
                      @click="console.log('DELETING')"
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
import { ref, computed } from "vue";
import axios from "axios";
import { HubsList } from "@/modules/hubs/types";

const hubList = ref<HubsList[]>([]);
const searchValue = ref<string>("");

const setup = async () => {
  let data = await axios.get("http://localhost:5000/hub", {
    withCredentials: true,
  });

  console.log(data.data);
  hubList.value = data.data;
  // hubList.value = [
  //   {
  //     HubID: "1",
  //     HubName: "OMGAND",
  //     PermissionLevel: 5,
  //   },
  //   {
  //     HubID: "1",
  //     HubName: "OMGAND",
  //     PermissionLevel: 4,
  //   },
  //   {
  //     HubID: "1",
  //     HubName: "OMGAND",
  //     PermissionLevel: 3,
  //   },
  //   {
  //     HubID: "1",
  //     HubName: "OMGAND",
  //     PermissionLevel: 2,
  //   },
  //   {
  //     HubID: "1",
  //     HubName: "OMGAND",
  //     PermissionLevel: 1,
  //   },
  //   {
  //     HubID: "1",
  //     HubName: "OMGAND",
  //     PermissionLevel: 5,
  //   },
  //   {
  //     HubID: "1",
  //     HubName: "OMGAND",
  //     PermissionLevel: 4,
  //   },
  //   {
  //     HubID: "1",
  //     HubName: "OMGAND",
  //     PermissionLevel: 3,
  //   },
  //   {
  //     HubID: "1",
  //     HubName: "OMGAND",
  //     PermissionLevel: 2,
  //   },
  //   {
  //     HubID: "1",
  //     HubName: "OMGAND",
  //     PermissionLevel: 1,
  //   },
  //   {
  //     HubID: "1",
  //     HubName: "OMGAND",
  //     PermissionLevel: 5,
  //   },
  //   {
  //     HubID: "1",
  //     HubName: "OMGAND",
  //     PermissionLevel: 4,
  //   },
  //   {
  //     HubID: "1",
  //     HubName: "OMGAND",
  //     PermissionLevel: 3,
  //   },
  //   {
  //     HubID: "1",
  //     HubName: "OMGAND",
  //     PermissionLevel: 2,
  //   },
  //   {
  //     HubID: "1",
  //     HubName: "OMGAND",
  //     PermissionLevel: 1,
  //   },
  // ];
};

const filteredHubs = computed(() => {
  let filter = hubList.value;
  return filter.filter((hub) => hub.HubName.includes(searchValue.value));
});

setup();
</script>

<style lang="scss">
.main-hub-list-viewer {
  display: flex;
  flex-grow: 1;
  background-color: rgb(32, 38, 62);
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

.hub-card {
  background-color: rgb(36, 42, 66);
}
</style>
