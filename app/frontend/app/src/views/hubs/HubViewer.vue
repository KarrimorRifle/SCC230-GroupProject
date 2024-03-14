<template>
  <div class="main-hub-viewer mx-xl-5 d-flex">
    <div class="container-fluid flex-grow-1">
      <div
        class="row hub-row px-0"
        style="min-height: 0; max-height: 100%; height: 100%"
      >
        <div class="col-3 text-start bg-dark px-0">
          <div class="container-fluid sub-nav text-light">
            <div class="row text-light">
              <button
                class="btn btn-secondary border-2 text-light rounded-top-0 rounded-end-0"
                @click="router.push('/hubs')"
              >
                <b>{{ "< Hubs" }}</b>
              </button>
            </div>
            <div class="row">
              <h3 class="text-center mt-2 border-bottom mb-0">
                <b>NAV</b>
              </h3>
            </div>
            <div
              class="row sub-nav-item"
              :class="{ 'active hub-main-bg': location == 'users' }"
            >
              <button @click="location = 'users'">
                Users {{ location == "users" ? ">" : "" }}
              </button>
            </div>
            <div
              class="row sub-nav-item"
              :class="{ 'active hub-main-bg': location == 'devices' }"
            >
              <button @click="location = 'devices'">
                Devices {{ location == "devices" ? ">" : "" }}
              </button>
            </div>
            <div
              class="row sub-nav-item"
              :class="{ 'active hub-main-bg': location == 'schedules' }"
            >
              <button @click="location = 'schedules'">
                Schedules {{ location == "schedules" ? ">" : "" }}
              </button>
            </div>
          </div>
        </div>
        <div class="col-9 px-0 hub-main-bg d-flex flex-column">
          <div
            class="container-fluid container text-light d-flex flex-column flex-grow-1"
            v-if="hub"
          >
            <div class="row pb-2">
              <h2 class="text-lg-start text-middle mb-0 ps-3 col-lg-8 col-12">
                <permissions-icon :permission-level="hub.PermissionLevel" />
                <b class="pt-4">
                  {{
                    hub.PermissionLevel >= 4
                      ? " HUB PAGE"
                      : " HUB PAGE: " + hub.HubName
                  }}
                </b>
              </h2>
              <div
                v-if="hub.PermissionLevel == 5"
                class="col-lg-4 col-12 d-flex justify-content-lg-end justify-content-start p-lg-0 pe-lg-2 pb-3 ps-4"
              >
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
            <div class="row px-3" v-if="hub.PermissionLevel >= 4">
              <div class="container-fluid">
                <div class="input-group">
                  <div class="input-group-text">Name</div>
                  <input
                    type="text"
                    class="form-control"
                    v-model="hub.HubName"
                  />
                  <button
                    class="input-group-text btn btn-success"
                    @click="updateHubName()"
                  >
                    Update Name
                  </button>
                </div>
              </div>
            </div>
            <div class="row m-0 p-0 px-4">
              <hr class="seperator text-light px-4 mt-3 m-0" />
            </div>
            <div
              class="row main-container mx-0 px-0 flex-grow-1"
              style="min-height: 0; max-height: 100%; height: 100%"
            >
              <div class="container-fluid d-flex flex-column">
                <user-list
                  :permission-level="hub.PermissionLevel"
                  v-if="location == 'users'"
                />
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
import UserList from "./pages/UserList.vue";
import PermissionsIcon from "./components/PermissionsIcon.vue";

const hub = ref<HubBase>();
const notif = ref<typeof NotificationModule>();
const deleting = ref<boolean>(false);
const deletingHubName = ref<string>("");

const location = ref<"users" | "devices" | "schedules">("users");

let hubID = router.currentRoute.value.params.id;
const setup = async () => {
  let data = await axios.get(`http://localhost:5000/hub/${hubID}`, {
    withCredentials: true,
  });

  console.log(data.data);
  hub.value = data.data;

  let tempLocation = router.currentRoute.value.query.tempLocation;
  if (tempLocation != undefined && typeof tempLocation == "string")
    if (["users", "devices", "schedules"].includes(tempLocation.toLowerCase()))
      location.value = tempLocation.toLowerCase();
    else
      notif.value?.show(
        "Invalid sublocation!",
        "The location you are trying to reach is invalid",
        "warning"
      );
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
  min-height: 0;
}

.hub-main-bg {
  background-color: rgb(32, 38, 62);
}

.main-hub-viewer > div {
  max-height: 100%;
}

div {
  min-height: 0;
  max-height: 100%;
}

.sub-nav-item {
  & > button {
    border-left: 0px;
    border-right: 0px;
    border-bottom: 1px solid rgb(74, 88, 89);
    border-top: none;
    background: rgba(0, 0, 0, 0);
    padding: 0.8rem 0rem;
    font-size: 1.3rem;
    font-style: none;
    color: gray;
    font-weight: 100 !important;
  }

  &.active > button {
    border-top: 1px solid white;
    border-bottom: 1px solid white;
    font-weight: 700 !important;
    color: white;
  }
}
</style>
