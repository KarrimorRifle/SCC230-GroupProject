<template>
  <div class="main-hub-viewer mx-xl-5 d-flex">
    <div class="container-fluid flex-grow-1">
      <div
        class="row hub-row px-0"
        style="min-height: 0; max-height: 100%; height: 100%"
      >
        <div class="col-3 text-start bg-dark px-0">
          <div class="container-fluid">
            <div class="row text-light">
              <button
                class="btn btn-secondary border-2 text-light"
                @click="router.push('/hubs')"
              >
                <b>{{ "< Hubs" }}</b>
              </button>
            </div>
          </div>
        </div>
        <div class="col-9 px-0">
          <div class="container-fluid text-light" v-if="hub">
            <div class="row d-flex justify-content-between mb-3 mt-2">
              <h2 class="text-start mb-0 ps-3 col-6">
                <b v-if="hub.PermissionLevel >= 4">HUB PAGE</b>
                <b v-else>HUB PAGE: {{ hub.HubName }}</b>
              </h2>
              <div class="col-6 d-flex justify-content-end">
                <div class="input-group" v-if="deleting">
                  <input
                    type="text"
                    placeholder="Enter name of hub"
                    class="form-control"
                    v-model="deletingHubName"
                  />
                  <button
                    class="input-group-text btn btn-danger"
                    @click="deleteHub()"
                  >
                    DELETE
                  </button>
                  <button
                    class="input-group-text btn btn-secondary"
                    @click="deleting = false"
                  >
                    Cancel
                  </button>
                </div>
                <button class="btn btn-danger" v-else @click="deleting = true">
                  DELETE
                </button>
              </div>
            </div>
            <div class="row" v-if="hub.PermissionLevel >= 4">
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
  <notification-module ref="notif" />
</template>

<script setup lang="ts">
import { ref } from "vue";
import axios, { AxiosError } from "axios";
import { HubBase } from "@/modules/hubs/types";
import router from "@/router";
import NotificationModule from "@/components/NotificationModule.vue";

const hub = ref<HubBase>();
const notif = ref<typeof NotificationModule>();
const deleting = ref<boolean>(false);
const deletingHubName = ref<string>("");

let hubID = router.currentRoute.value.params.id;
const setup = async () => {
  let data = await axios.get(`http://localhost:5000/hub/${hubID}`, {
    withCredentials: true,
  });

  console.log(data.data);
  hub.value = data.data;
};

const updateHubName = async () => {
  let data = await axios
    .patch(`http://localhost:5000/hub/${hubID}`, hub.value, {
      withCredentials: true,
    })
    .catch((e) => {
      console.log(e);
    });
  hub.value = data.data;
  notif.value?.show(
    "Updated hub title",
    "Your hub title has been succesfully updated",
    "success"
  );
};

const deleteHub = () => {
  if (deletingHubName.value != hub.value?.HubName) {
    notif.value?.show(
      "Delete unsuccesful",
      "The input doesn't match the hub's name",
      "danger"
    );
    return;
  }
  axios
    .delete(`http://localhost:5000/hub/${hubID}`, {
      withCredentials: true,
    })
    .then(() => {
      router.push("/hubs");
    })
    .catch((e: AxiosError) => {
      if (e.code == "500") console.log(e);
      else {
        notif.value?.show("Delete unsuccesful", e.message, "danger");
        return;
      }
    });
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
