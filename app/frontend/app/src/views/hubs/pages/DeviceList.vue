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
        <div class="card-body container-fluid py-2">
          <h5 class="p-0 m-0 text-start"><b>Add Device</b></h5>
          <div class="input-group mb-2">
            <div class="input-group-text">Name</div>
            <input
              type="text"
              class="form-control"
              v-model="newDevice.DeviceName"
            />
          </div>
          <div class="row">
            <div class="col-3">
              <div class="input-group">
                <div class="input-group-text">Type</div>
                <input
                  type="text"
                  class="form-control"
                  v-model="newDevice.DeviceType"
                />
              </div>
            </div>
            <div class="col-8 ps-0">
              <div class="input-group">
                <div class="input-group-text">IP</div>
                <input
                  type="text"
                  class="form-control"
                  v-model="newDevice.IpAddress"
                />
              </div>
            </div>
            <div class="col-1 px-0">
              <button class="btn btn-success" @click="addNewDevice">
                Submit
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <notification-module ref="notif" />
</template>
<script setup lang="ts">
import { ref } from "vue";
import { HubDevice, NewHubDevice } from "@/modules/hubs/types";
import axios from "axios";
import router from "@/router";
import NotificationModule from "@/components/NotificationModule.vue";

const notif = ref<typeof NotificationModule>();
const devices = ref<HubDevice[]>([]);
const searchMode = ref<string>("name");
const searchValue = ref<string>("");

const addItem = ref<boolean>(true);
const newDevice = ref<NewHubDevice>({
  DeviceName: "",
  DeviceType: "",
  IpAddress: "",
});

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

const addNewDevice = async () => {
  let data = await axios
    .post(`http://localhost:5000/hub/${HubID}/device`, newDevice, {
      withCredentials: true,
    })
    .catch((e) => {
      console.log(e);
      notif.value?.show(
        "Unable to add device",
        "Something went wrong, check values are valid or try again later",
        "danger"
      );
      return;
    });

  console.log(data);
  if (data && data.request.status == 200)
    notif.value?.show(
      "Device added",
      "We was able to add your device to the system",
      "success"
    );
  else
    notif.value?.show(
      "Unable to add device",
      "Something went wrong, check values are valid or try again later",
      "danger"
    );

  setup();
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
