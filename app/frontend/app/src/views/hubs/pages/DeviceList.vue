<template>
  <div class="hub-device-list-viewer container-fluid flex-grow-1 pt-3">
    <div class="row">
      <div class="input-group col-12" :class="{ 'rounded-bottom-0': addItem }">
        <input
          class="form-control"
          :class="{ 'rounded-bottom-0': addItem }"
          type="text"
        />
        <button
          class="input-group-text dropdown-toggle"
          data-bs-toggle="dropdown"
          aria-expanded="false"
        >
          Search by:
          {{ searchMode.charAt(0).toUpperCase() + searchMode.slice(1) }}
        </button>
        <ul class="dropdown-menu">
          <li>
            <button class="dropdown-item" @click="searchMode = 'name'">
              Name
            </button>
          </li>
          <li>
            <button class="dropdown-item" @click="searchMode = 'company'">
              Company
            </button>
          </li>
        </ul>
        <button
          class="input-group-text btn"
          :class="addItem ? 'btn-danger rounded-bottom-0' : 'btn-secondary'"
          @click="addItem = !addItem"
        >
          {{ addItem ? "x" : "+" }}
        </button>
      </div>
      <div v-if="addItem" class="col-12 card border-top-0">
        <div class="card-body">hello</div>
      </div>
    </div>
  </div>
  <notification-module ref="notif" />
</template>
<script setup lang="ts">
import { ref } from "vue";
import { HubDevice } from "@/modules/hubs/types";
import axios from "axios";
import router from "@/router";
import NotificationModule from "@/components/NotificationModule.vue";

const notif = ref<typeof NotificationModule>();
const devices = ref<HubDevice[]>([]);
const searchMode = ref<string>("name");
const searchValue = ref<string>("");

const addItem = ref<boolean>(false);

const HubID = router.currentRoute.value.params.id;
const setup = async () => {
  let data = await axios
    .get(`http://localhost:5000/hub/${HubID}/device`, {
      withCredentials: true,
    })
    .catch((e) => {
      notif.value?.show(
        "Couldn't fetch devices",
        "Unable to get devices, try again later",
        "warning"
      );
      console.log(e);
      return;
    });
  console.log(data.data);
  devices.value = data.data;
};

setup();
</script>
<style lang="scss">
div.hub-device-list-viewer {
  min-height: 0;
  max-height: 100%;
  height: 100%;
  overflow-y: auto;
  overflow-x: hidden;
}
</style>
