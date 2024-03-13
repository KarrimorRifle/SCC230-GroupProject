<template>
  <div class="hub-device-list-viewer container-fluid flex-grow-1 pt-3">
    <div class="row">
      <div class="mt-3"></div>
      <div class="card">
        <div
          v-for="device in devices"
          :key="device.DeviceID"
          class="row card-body mb-2 mx-3"
        >
          <div class="col-6 text-start ps-3">
            {{ device.DeviceName }}
          </div>
        </div>
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
