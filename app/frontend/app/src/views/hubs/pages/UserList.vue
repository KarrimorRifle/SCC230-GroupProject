<template>
  <div class="hub-user-list-viewer container-fluid flex-grow-1 pt-3">
    <div class="row">
      <div class="input-group">
        <input
          type="text"
          class="form-control"
          placeholder="Find user by name"
        />
        <div class="input-group-text">Sort by:</div>
        <button class="input-group-text dropdown-toggle">Privelage: ASC</button>
      </div>
    </div>
    <div class="mt-3"></div>
    <div class="card">
      <div :key="account.AccountID" class="row card-body mb-2 mx-3">
        <div class="col-1">
          <button>
            <permissions-icon :permission-level="account.PermissionLevel" />
          </button>
        </div>
        <div class="col-6 text-start ps-3">
          {{ account.Name }}
        </div>
      </div>
    </div>
  </div>
  <notification-module ref="notif" />
</template>
<script setup lang="ts">
import { ref } from "vue";
import { HubUser } from "@/modules/hubs/types";
import axios from "axios";
import router from "@/router";
import NotificationModule from "@/components/NotificationModule.vue";
import PermissionsIcon from "../components/PermissionsIcon.vue";

const notif = ref<typeof NotificationModule>();
const accounts = ref<HubUser[]>([]);

const HubID = router.currentRoute.value.params.id;
const setup = async () => {
  let data = await axios
    .get(`http://localhost:5000/hub/${HubID}/user`, {
      withCredentials: true,
    })
    .catch((e) => {
      notif.value?.show(
        "Couldn't fetch users",
        "Unable to get users, try again later",
        "warning"
      );
      console.log(e);
      return;
    });

  let account = await axios.get("http://localhost:5000/accounts", {
    withCredentials: true,
  });
  // console.log(data.data);
  // console.log(account.data);
  accounts.value = data.data;
  accounts.value = accounts.value.filter(
    (item) => item.AccountID != account.data.AccountID
  );
};

setup();
</script>
<style lang="scss">
div.hub-user-list-viewer {
  min-height: 0;
  max-height: 100%;
  height: 100%;
  overflow-y: auto;
  overflow-x: hidden;
}
</style>
