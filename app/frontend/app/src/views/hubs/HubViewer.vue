<template>
  <div class="main-hub-viewer mx-xl-5">
    <div class="container-fluid">
      <p></p>
      <div class="row hub-row">
        <div class="col-3 text-start">
          <label
            for="hubName"
            class="px-3 text-light mt-2"
            style="margin: 0; padding: 0"
            >Hub Name:
          </label>
        </div>
        <div class="col-6">
          <input
            v-if="permissionLevel == 5"
            type="text"
            class="form-control"
            id="hubName"
            aria-describedby="emailHelp"
            placeholder="Hub Name"
            v-model="hubName"
          />
          <a
            v-if="permissionLevel != 5"
            id="HubName"
            class="px-3 text-light mt-2"
            style="margin: 0; padding: 0"
            >Hub Name Here
          </a>
        </div>
        <div class="col-2">
          <button
            v-if="permissionLevel == 5"
            class="btn btn-sm btn-outline-secondary me-2 text-light border-2 d-sm-block d-none"
            @click="updateHub()"
          >
            UPDATE
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import axios from "axios";

const hubName = ref();
const permissionLevel = ref();

const setup = async () => {
  let hubID = window.location.href.slice(-19);
  let data = await axios.get(`http://localhost:5000/hub/${hubID}`, {
    withCredentials: true,
  });

  console.log(data.data);
  hubName.value = data.data.HubName;
  permissionLevel.value = data.data.PermissionLevel;
  document.getElementById("HubName").innerHTML = hubName.value;
};

const updateHub = async () => {
  let hubID = window.location.href.slice(-19);
  await axios.patch(
    `http://localhost:5000/hub/${hubID}`,
    {
      HubName: `${document.getElementById("hubName").value}`,
    },
    {
      withCredentials: true,
    }
  );
  setup();
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
