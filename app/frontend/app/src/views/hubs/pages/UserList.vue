<template>
  <div class="hub-user-list-viewer container-fluid flex-grow-1 pt-3">
    <div class="row">
      <div class="input-group">
        <button class="input-group-text btn btn-success" @click="createToken()">
          +
        </button>
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
    <div class="row" v-if="accounts.length == 0">
      <div class="text-muted">Uh oh! looks like nothing is here...</div>
      <div class="text-muted">
        if this is unexpected call us on
        <a href="tel:07696969696">+44 7696 969696</a>
      </div>
    </div>
    <div class="card mb-2 mx-3 p-0" v-else>
      <div
        v-for="account in accounts"
        :key="account.AccountID"
        class="row card-body m-0 p-0"
      >
        <div class="col-1 px-0 border-end">
          <button
            class="container-fluid user-rank-selector py-2"
            :class="{
              'dropdown-toggle':
                permissionLevel >= 4 &&
                account.PermissionLevel < permissionLevel,
              disabled:
                permissionLevel <= 3 ||
                account.PermissionLevel > permissionLevel,
            }"
            :style="{
              cursor:
                permissionLevel >= 4 &&
                account.PermissionLevel < permissionLevel
                  ? 'pointer'
                  : 'default',
            }"
            data-bs-toggle="dropdown"
            aria-expanded="false"
          >
            <permissions-icon :permission-level="account.PermissionLevel" />
            <div class="d-inline ps-1"></div>
          </button>
          <ul
            class="dropdown-menu"
            id="level-setter"
            v-if="
              permissionLevel >= 4 && account.PermissionLevel < permissionLevel
            "
          >
            <li v-if="permissionLevel == 5">
              <button
                class="dropdown-item"
                @click="setPerm(4, account.AccountID, account.Name)"
              >
                <permissions-icon :permission-level="4" />
              </button>
            </li>
            <li>
              <button
                class="dropdown-item"
                @click="setPerm(3, account.AccountID, account.Name)"
              >
                <permissions-icon :permission-level="3" />
              </button>
            </li>
            <li>
              <button
                class="dropdown-item"
                @click="setPerm(2, account.AccountID, account.Name)"
              >
                <permissions-icon :permission-level="2" />
              </button>
            </li>
            <li>
              <button
                class="dropdown-item"
                @click="setPerm(1, account.AccountID, account.Name)"
              >
                <permissions-icon :permission-level="1" />
              </button>
            </li>
          </ul>
        </div>
        <div class="col-7 text-start ps-2">
          <b>{{ account.Name }}</b>
          <div class="text-muted">ID: {{ account.AccountID }}</div>
        </div>
        <div class="col-4 border-start">
          <button
            class="btn btn-outline-danger me-2 mt-2"
            @click="setPerm(0, account.AccountID, account.Name)"
          >
            Block
            <div class="d-inline ps-1"></div>
            <img
              src="@/assets/stop.svg"
              alt="Block user"
              style="max-width: 1.4rem"
            />
          </button>
          <button
            class="btn btn-sm btn-outline-danger me-2 mt-2"
            @click="remove(account.AccountID, account.Name)"
          >
            Remove
            <div class="d-inline ps-1"></div>
            <img
              src="@/assets/delete-svgrepo-com.svg"
              alt="Remove user"
              style="max-width: 1.5rem"
            />
          </button>
        </div>
      </div>
    </div>
  </div>
  <notification-module ref="notif" />
</template>
<script setup lang="ts">
import { ref, defineProps } from "vue";
import { HubUser } from "@/modules/hubs/types";
import axios from "axios";
import router from "@/router";
import NotificationModule from "@/components/NotificationModule.vue";
import PermissionsIcon from "../components/PermissionsIcon.vue";

const notif = ref<typeof NotificationModule>();
const accounts = ref<HubUser[]>([]);

const props = defineProps<{
  permissionLevel: number;
}>();

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

  accounts.value = data.data;
  accounts.value = accounts.value.filter(
    (item) => item.AccountID != account.data.AccountID
  );
};

const setPerm = async (level: number, id: string, name?: string) => {
  let data = await axios
    .patch(
      `http://localhost:5000/hub/${HubID}/user/${id}`,
      {
        PermissionLevel: level,
      },
      {
        withCredentials: true,
      }
    )
    .catch((e) => {
      console.log(e);
      notif.value?.show(
        "Unable to update permissions",
        "Soemthing went wrong, try again later",
        "danger"
      );
      return;
    });

  if (level != 0)
    notif.value?.show(
      "Account permission changed",
      `${name}'s permission level was adjusted!`,
      "success"
    );
  else
    notif.value?.show(
      "Account blocked",
      `${name}'s account has been BLOCKED`,
      "warning"
    );

  setup();
};

const remove = async (id: string, name: string) => {
  let data = await axios
    .delete(`http://localhost:5000/hub/${HubID}/user/${id}`, {
      withCredentials: true,
    })
    .catch((e) => {
      console.log(e);
      notif.value?.show(
        "Unable to remove person",
        "Soemthing went wrong, try again later",
        "danger"
      );
      return;
    });

  notif.value?.show(
    "Account removed",
    `${name}'s account has been taken off the hub`,
    "warning"
  );

  setup();
};

const createToken = async () => {
  let response = await axios
    .post(
      `http://localhost:5000/hub/${HubID}/invite`,
      {},
      {
        withCredentials: true,
      }
    )
    .catch((e) => {
      console.log(e);
      notif.value?.show(
        "Unable to create invite token",
        "Something went wrong, try again later",
        "danger"
      );
      return;
    });

  if (response && response.data) {
    const token = response.data;
    await navigator.clipboard.writeText(
      `http://localhost:8080/hubs?invite=true&hub=${token.HubID}&token=${token.Token}`
    );
    notif.value?.show(
      "Invite token created",
      "The invite link has been copied to your clipboard: usable for 24 hours",
      "success"
    );
  }
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

.user-rank-selector {
  background-color: rgba(0, 0, 0, 0);
  border: none;
}

#level-setter {
  max-width: 4rem !important;
  width: 4rem;
  min-width: 0;
}

.dropdown-item {
  padding: 0;
  display: flex;
  width: 100%;
  justify-content: center;
  padding-bottom: 0.5rem;
  padding-top: 0.5rem;
  border-bottom: 1px solid gray;
}

ul > li:last-of-type > .dropdown-item {
  border-bottom: 0px;
}
</style>
