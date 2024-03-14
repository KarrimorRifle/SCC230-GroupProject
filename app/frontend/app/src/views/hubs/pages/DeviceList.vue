<template>
  <div
    class="hub-device-list-viewer container-fluid d-flex flex-column flex-grow-1 pt-3"
  >
    <div class="row">
      <div class="input-group col-12" :class="{ 'rounded-bottom-0': addItem }">
        <input
          class="form-control"
          :class="{ 'rounded-bottom-0': addItem }"
          type="text"
          v-model="searchValue"
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
          :class="addItem ? 'btn-danger rounded-bottom-0' : 'btn-success'"
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
    <hr class="text-secondary mx-2" />
    <div class="flex-grow-1 container-fluid">
      <div class="row d-flex justify-content-center pt-5 mt-5" v-if="loading">
        <div class="spinner-border mt-2" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      <div class="row" v-else-if="devices.length == 0">
        <div class="text-muted">Uh oh! looks like nothing is here...</div>
        <div class="text-muted">
          if this is unexpected call us on
          <a href="tel:07696969696">+44 7696 969696</a>
        </div>
      </div>
      <div
        class="card container"
        v-for="device in devices"
        :key="device.DeviceID"
      >
        <div class="row card-body py-0">
          <div class="col-4 text-start py-1 border-end">
            <b>{{ device.DeviceName }}</b>
          </div>
          <div class="col-5 text-start py-1 border-end">
            <div><b>Company:</b> {{ device.Company }}</div>
            <div class="text-muted"><b>ID:</b> {{ device.DeviceID }}</div>
          </div>
          <div class="col-3">
            <button
              class="btn btn-outline-secondary text-light border-2 mt-2 me-2"
              @click="editDevice(device.DeviceID)"
            >
              EDIT
            </button>
            <button class="btn btn-outline-danger text-light border-2 mt-2" @click="deleteDevice(device.DeviceID)">
              DELETE
            </button>
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

const loading = ref<boolean>(true);

const notif = ref<typeof NotificationModule>();
const devices = ref<HubDevice[]>([]);
const searchMode = ref<string>("name");
const searchValue = ref<string>("");

const addItem = ref<boolean>(false);
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
  loading.value = false;
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

const editDevice = (id: string) => {
  console.log("edit");
}

const deleteDevice = (id: string) => {
  console.log("delete");
}

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
