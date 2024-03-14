<template>
  <div class="main-hub-list-viewer mx-xl-5">
    <div class="container-fluid">
      <div class="row hub-list-row">
        <div class="col-3 text-light">
          <h3 class="my-3">FILTERS</h3>
          <hr class="mt-0" />
          <div class="container">
            <h4>Sort by</h4>
            <div class="input-group mb-2">
              <div class="input-group-text">
                <img
                  src="@/assets/permissions/lvl.svg"
                  style="max-width: 1.5rem"
                />
              </div>
              <select id="privilage" class="form-select" v-model="sortRank">
                <option value="NONE" selected>NONE</option>
                <option value="ASC">ASC</option>
                <option value="DESC">DESC</option>
              </select>
            </div>
            <div class="input-group">
              <div class="input-group-text">
                <img src="@/assets/user.svg" style="max-width: 1.5rem" />
              </div>
              <select id="privilage" class="form-select" v-model="sortCount">
                <option value="NONE" selected>NONE</option>
                <option value="ASC">ASC</option>
                <option value="DESC">DESC</option>
              </select>
            </div>
          </div>
          <hr />
          <h4>
            <img src="@/assets/permissions/lvl.svg" style="max-width: 1.5rem" />
            Permission Level
          </h4>
          <table id="ranks">
            <tr>
              <td>
                <img
                  src="@/assets/permissions/5.svg"
                  style="max-width: 1.5rem"
                />
              </td>
              <td>Owner</td>
            </tr>
            <tr>
              <td>
                <img
                  src="@/assets/permissions/4.svg"
                  style="max-width: 1.5rem"
                />
              </td>
              <td>Admin</td>
            </tr>
            <tr>
              <td>
                <img
                  src="@/assets/permissions/3.svg"
                  style="max-width: 1.5rem"
                />
              </td>
              <td>Scheduler</td>
            </tr>
            <tr>
              <td>
                <img
                  src="@/assets/permissions/2.svg"
                  style="max-width: 1.5rem"
                />
              </td>
              <td>Enabler</td>
            </tr>
            <tr>
              <td>
                <img
                  src="@/assets/permissions/1.svg"
                  style="max-width: 1.5rem"
                />
              </td>
              <td>Viewer</td>
            </tr>
          </table>
        </div>
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
            <button
              class="btn btn-outline-primary border-2 text-light"
              @click="makeHub()"
            >
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
                    class="col-1 d-md-flex d-none border-end ps-4 justify-content-center align-items-center"
                    style="font-size: 1.3rem"
                  >
                    <div class="me-2">
                      {{ hub.UserCount }}
                    </div>
                    <img src="@/assets/user.svg" style="max-width: 1.2rem" />
                  </div>
                  <div
                    class="col-md-1 col-2"
                    :class="{
                      'my-1': hub.PermissionLevel != 5,
                      'mt-2': hub.PermissionLevel == 5,
                    }"
                  >
                    <permissions-icon :permission-level="hub.PermissionLevel" />
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
                    class="col-xxl-2 col-xl-3 col-lg-3 col-md-4 col-4 ps-2 py-2 border-start d-flex"
                    v-if="hub.PermissionLevel == 5"
                  >
                    <button
                      class="btn btn-sm btn-outline-secondary me-2 text-light border-2 d-sm-block d-none"
                      @click="router.push(`/hubs/${hub.HubID}`)"
                    >
                      <!-- when able make it so that the you can edit in list-->
                      EDIT
                    </button>
                    <button
                      class="btn btn-sm btn-outline-danger text-light border-2"
                      @click="deleteHub(hub.HubID)"
                    >
                      DELETE
                    </button>
                  </div>
                  <div
                    class="col-xxl-1 col-md-2 col-4 ps-2 py-2 border-start d-flex"
                    v-else
                  >
                    <button
                      class="btn btn-sm btn-outline-danger text-light border-2"
                      @click="leaveHub(hub.HubID)"
                    >
                      LEAVE
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <div class="text-muted mt-4" v-if="hubList.length == 0">
              Uh Oh! Looks like there is nothing here!<br />
              If this is unexpected please contact IOTA support at +44 69696969
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <notification-module ref="notif" />
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import axios from "axios";
import { HubsList } from "@/modules/hubs/types";
import router from "@/router";
import PermissionsIcon from "./components/PermissionsIcon.vue";
import NotificationModule from "@/components/NotificationModule.vue";

const hubList = ref<HubsList[]>([]);
const searchValue = ref<string>("");
const notif = ref<typeof NotificationModule>();

//sorting menu
const sortRank = ref<"NONE" | "ASC" | "DESC">("NONE");
const sortCount = ref<"NONE" | "ASC" | "DESC">("NONE");

const setup = async () => {
  let data = await axios.get("http://localhost:5000/hub", {
    withCredentials: true,
  });

  console.log(data.data);
  hubList.value = data.data;

  if (
    router.currentRoute.value.query.invite == "true" &&
    typeof router.currentRoute.value.query.token == "string"
  )
    joinHub(router.currentRoute.value.query.token);
};

const filteredHubs = computed(() => {
  let filter = hubList.value;

  if (sortCount.value != "NONE")
    filter.sort((hub1, hub2) =>
      sortCount.value == "ASC"
        ? hub1.UserCount - hub2.UserCount
        : hub2.UserCount - hub1.UserCount
    );

  if (sortRank.value != "NONE")
    filter.sort((hub1, hub2) =>
      sortRank.value == "ASC"
        ? hub1.PermissionLevel - hub2.PermissionLevel
        : hub2.PermissionLevel - hub1.PermissionLevel
    );

  return filter.filter((hub) => hub.HubName.includes(searchValue.value));
});

const makeHub = async () => {
  let data = await axios
    .post(
      "http://localhost:5000/hub",
      {
        HubName: `HUB ${hubList.value.length}`,
      },
      {
        withCredentials: true,
      }
    )
    .catch((e) => {
      console.log(e);
      notif.value?.show(
        "Couln't make hub",
        "Server error, try again later",
        "warning"
      );
    });

  if (data && data.data) {
    console.log(data);
    await navigator.clipboard.writeText(
      `http://localhost:8080/hubs/${data.data.HubID}`
    );
    notif.value?.show(
      "Hub created",
      `Created hub, ${data.data.HubID}! link copied to clipboard!`,
      "success"
    );
  }
  setup();
};

const deleteHub = async (id: string) => {
  await axios
    .delete(`http://localhost:5000/hub/${id}`, {
      withCredentials: true,
    })
    .catch((e) => {
      console.log(e);
      notif.value?.show(
        "Couln't delete hub",
        "Server error, try again later",
        "warning"
      );
    });
  notif.value?.show(
    "Hub deleted",
    "Succesfully able to removed hub",
    "success"
  );
  setup();
};

const leaveHub = async (id: string) => {
  await axios
    .delete(`http://localhost:5000/hub/${id}/user`, {
      withCredentials: true,
    })
    .catch((e) => {
      console.log(e);
      notif.value?.show(
        "Couln't leave hub",
        "Server error, try again later",
        "warning"
      );
    });
  notif.value?.show("Hub left", "Succesfully able to leave hub", "success");

  setup();
};

const joinHub = async (HubToken: string) => {
  let data = await axios
    .post(
      `http://localhost:5000/hub/invite/${HubToken}`,
      {},
      {
        withCredentials: true,
      }
    )
    .catch((e) => {
      console.log(e);
      if (e.code == "500")
        notif.value?.show(
          "Unable to join hub!",
          "Something went wrong, try again later"
        );
      else
        notif.value?.show(
          "Unable to join hub!",
          "Something went wrong, try again later"
        );
      return;
    });

  if (data && data.data) router.push(`/hubs/${data.data.HubID}`);
  else
    notif.value?.show(
      "WHAT!",
      "Something strange happened? check if you did join the hub via the list!"
    );
};

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

#ranks td:nth-child(1) {
  width: 30%;
  text-align: start;
  padding-left: 1rem;
}

#ranks tr {
  border-bottom: 1px;
  border-style: solid;
  height: 2rem;
  width: 100%;
}

#ranks {
  width: 100%;
}

#ranks td:nth-child(2) {
  width: 70%;
  text-align: start;
}
</style>
