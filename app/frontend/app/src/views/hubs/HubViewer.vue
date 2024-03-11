<template>
  <div class="main-hub-viewer mx-xl-5">
    <div class="container-fluid">
      <div class="row hub-row">
        <div class="col-3 text-light">hi</div>
        <div class="col bg-dark d-flex flex-column">hello</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import axios from "axios";
import { HubsList } from "@/modules/hubs/types";

const hubList = ref<HubsList[]>([]);
const searchValue = ref<string>("");

//sorting menu
const sortRank = ref<"NONE" | "ASC" | "DESC">("NONE");
const sortCount = ref<"NONE" | "ASC" | "DESC">("NONE");

const setup = async () => {
  let data = await axios.get("http://localhost:5000/hub", {
    withCredentials: true,
  });

  console.log(data.data);
  hubList.value = data.data;
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
  await axios.post(
    "http://localhost:5000/hub",
    {
      HubName: `HUB ${hubList.value.length}`,
    },
    {
      withCredentials: true,
    }
  );
  setup();
};

const deleteHub = async (id: string) => {
  await axios.delete(`http://localhost:5000/hub/${id}`, {
    withCredentials: true,
  });
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
