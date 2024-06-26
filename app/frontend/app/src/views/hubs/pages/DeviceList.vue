<template>
  <template v-if="!editing">
    <div
      class="hub-device-list-viewer container-fluid d-flex flex-column flex-grow-1 pt-3"
    >
      <div class="row">
        <div
          class="input-group col-12"
          :class="{ 'rounded-bottom-0': addItem }"
        >
          <input
            class="form-control"
            :class="{ 'rounded-bottom-0': addItem }"
            type="text"
            v-model="searchValue"
            v-on:keyup="filterDevices()"
            placeholder="Find device"
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
            v-if="permissionLevel >= 4"
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
          class="card container mb-2"
          v-for="device in devices"
          :key="device.DeviceID"
        >
          <div class="row card-body py-0">
            <div class="col-4 text-start py-1 border-end">
              <b>{{ device.DeviceName }}</b>
            </div>
            <div class="col text-start py-1 border-end">
              <div><b>Company:</b> {{ device.Company }}</div>
              <div class="text-muted"><b>ID:</b> {{ device.DeviceID }}</div>
            </div>
            <div class="col-3" v-if="permissionLevel >= 4">
              <button
                class="btn btn-outline-secondary text-light border-2 mt-2 me-2"
                @click="editDevice(device.DeviceID)"
              >
                EDIT
              </button>
              <button
                class="btn btn-outline-danger text-light border-2 mt-2"
                @click="deleteDevice(device.DeviceID)"
              >
                DELETE
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  <template v-else>
    <div
      class="hub-device-list-viewer container-fluid d-flex flex-column flex-grow-1 pt-3"
      v-if="editingDevice"
    >
      <h3>Edit Device Details</h3>
      <div class="row mb-2">
        <div class="col-12 col-lg-6 mb-2 mb-lg-0 pe-0">
          <div class="input-group">
            <div class="input-group-text">Name</div>
            <input class="form-control" v-model="editingDevice.DeviceName" />
          </div>
        </div>
        <div class="col-12 col-lg-6 pe-0">
          <div class="input-group">
            <div class="input-group-text">ID</div>
            <input class="form-control" v-model="editingDevice.DeviceID" />
          </div>
        </div>
      </div>
      <div class="row mb-2">
        <div class="col-12 col-lg-6 mb-2 mb-lg-0 pe-0">
          <div class="input-group">
            <div class="input-group-text">IP</div>
            <input class="form-control" v-model="editingDevice.IpAddress" />
          </div>
        </div>
        <div class="col-12 col-lg-6 pe-0">
          <div class="input-group">
            <div class="input-group-text">Company</div>
            <input class="form-control" v-model="editingDevice.Company" />
          </div>
        </div>
      </div>
      <div class="row mb-2">
        <div class="col-12 col-lg-6 mb-2 mb-lg-0 pe-0">
          <div class="input-group">
            <div class="input-group-text">Key</div>
            <input class="form-control" v-model="editingDevice.Key" />
          </div>
        </div>
        <div class="col-12 col-lg-6 pe-0">
          <div class="input-group">
            <div class="input-group-text">version</div>
            <input
              class="form-control"
              type="number"
              step="0.1"
              v-model="editingDevice.Version"
            />
          </div>
        </div>
      </div>
      <div class="row">
        <div>
          <button
            class="btn btn-secondary me-2"
            @click="
              editingDevice = undefined;
              editing = false;
              setup();
            "
          >
            Cancel
          </button>
          <button class="btn btn-success" @click="saveDevice">Save</button>
        </div>
      </div>
    </div>
    <div v-else>
      <div class="spinner-border mt-5" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
  </template>
  <notification-module ref="notif" />
</template>
<script setup lang="ts">
import { ref, defineProps } from "vue";
import { HubDevice, NewHubDevice, EditingDevice } from "@/modules/hubs/types";
import axios from "axios";
import router from "@/router";
import NotificationModule from "@/components/NotificationModule.vue";

const loading = ref<boolean>(true);
const editing = ref<boolean>(false);
const editingDevice = ref<EditingDevice>();

const notif = ref<typeof NotificationModule>();
const devices = ref<HubDevice[]>([]);
const alldevices = ref<HubDevice[]>([]);
const searchMode = ref<string>("name");
const searchValue = ref<string>("");

const addItem = ref<boolean>(false);
const newDevice = ref<NewHubDevice>({
  DeviceName: "",
  DeviceType: "",
  IpAddress: "",
});

const props = defineProps<{
  permissionLevel: number;
}>();

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
  alldevices.value = data.data;
  filterDevices();
};

const filterDevices = async () => {
  if (searchMode.value == "name") {
    devices.value = alldevices.value.filter((item) =>
      item.DeviceName.toUpperCase().includes(searchValue.value.toUpperCase())
    );
    loading.value = false;
  } else {
    devices.value = alldevices.value.filter((item) =>
      item.Company.toUpperCase().includes(searchValue.value.toUpperCase())
    );
    loading.value = false;
  }
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

const editDevice = async (id: string) => {
  let request = await axios
    .get(`http://localhost:5000/hub/${HubID}/device/${id}`, {
      withCredentials: true,
    })
    .catch((e) => {
      console.log(e);
      notif.value?.show(
        "Unable to get device data",
        "Unable to retrieve data on the device, try again later",
        "warning"
      );
      return;
    });

  if (request && request.request.status == 200) {
    console.log(request.data);
    editingDevice.value = request.data;
    editing.value = true;
    return;
  } else
    notif.value?.show(
      "Unable to get device data",
      "Unable to retrieve data on the device, try again later",
      "warning"
    );
};

const deleteDevice = (id: string) =>
  axios
    .delete(`http://localhost:5000/hub/${HubID}/device/${id}`, {
      withCredentials: true,
    })
    .then((response) => {
      if (response.request.status == 200)
        notif.value?.show(
          "Device added",
          "Your device was added to the hub!",
          "success"
        );
      else
        notif.value?.show(
          "Something weird happened...",
          "Something went wrong, try again later",
          "warning"
        );
      setup();
    })
    .catch((e) => {
      console.log(e);
      notif.value?.show(
        "Unable to remove device",
        "Something went wrong, try again later",
        "danger"
      );
    });

const saveDevice = async () => {
  delete editingDevice.value["Vars"];
  let data = await axios
    .patch(
      `http://localhost:5000/hub/${HubID}/device/${editingDevice.value?.DeviceID}`,
      editingDevice.value,
      {
        withCredentials: true,
      }
    )
    .catch((e) => {
      console.log(e);
      notif.value?.show(
        "Couldn't save device",
        "Something happened, try again later",
        "danger"
      );
      return;
    });

  if (data && data.request.status == 200) {
    notif.value?.show(
      "Device saved",
      "Your device's details have been successfully updated",
      "success"
    );
    editingDevice.value = undefined;
    editing.value = false;
    setup();
    return;
  } else {
    notif.value?.show(
      "Couldn't save device",
      "Something happened, try again later",
      "danger"
    );
  }
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
