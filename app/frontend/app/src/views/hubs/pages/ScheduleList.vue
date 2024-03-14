<template>
  <template v-if="!loading">
    <div
      class="hub-schedule-list-viewer container-fluid d-flex flex-column flex-grow-1 pt-3"
      v-if="schedules"
    >
      <div class="row mb-2">
        <div class="input-group">
          <div class="input-group-text">Sort by:</div>
          <button class="input-group-text dropdown-toggle rounded-0">
            Rating: n/a
          </button>
          <div class="input-group-text">to be populated...</div>
        </div>
      </div>
      <div class="row">
        <div class="input-group">
          <input
            type="text"
            class="form-control"
            placeholder="Name of schedule"
          />
          <button class="input-group-text btn btn-success">+</button>
        </div>
      </div>
      <div class="row mt-3" v-if="schedules && schedules.length == 0">
        <div class="text-muted">Uh oh! looks like nothing is here...</div>
        <div class="text-muted">
          if this is unexpected call us on
          <a href="tel:07696969696">+44 7696 969696</a>
        </div>
      </div>
      <template v-else>
        <div>hello</div>
      </template>
    </div>
  </template>
  <template v-else>
    <div class="container-fluid d-flex justify-content-center mt-5">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
  </template>
  <notification-module ref="notif" />
</template>
<script setup lang="ts">
import { HubScheduleList } from "@/modules/hubs/types";
import NotificationModule from "@/components/NotificationModule.vue";
import router from "@/router";
import axios from "axios";
import { ref } from "vue";

const schedules = ref<HubScheduleList[]>();
const loading = ref<boolean>(true);
const notif = ref<typeof NotificationModule>();

const HubID = router.currentRoute.value.params.id;
const setup = async () => {
  loading.value = true;
  let data = await axios
    .get(`http://localhost:5000/hub/${HubID}/schedule`, {
      withCredentials: true,
    })
    .catch((e) => {
      console.log(e);
      notif.value?.show(
        "Couldn't load schedules",
        "Something went wrong, try again later",
        "danger"
      );
    });

  if (data && data.request.status == 200) {
    console.log(data.data);
    schedules.value = data.data;
    loading.value = false;
  } else {
    notif.value?.show(
      "Couldn't load schedules",
      "Something went wrong, try again later",
      "danger"
    );
  }
};

setup();
</script>
<style lang="scss">
div.hub-shcedule-list-viewer {
  min-height: 0;
  max-height: 100%;
  height: 100%;
  overflow-y: auto;
  overflow-x: hidden;
}
</style>
