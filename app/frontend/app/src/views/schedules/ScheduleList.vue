<template>
  <div class="main-container d-flex">
    <div class="main row bg-dark">
      <div class="col-2 options bg-secondary"></div>
      <div class="col-10 schedules px-0">
        <h2 class="text-start text-light underlined bg-dark px-3 py-2">
          Schedules
        </h2>
        <div class="buttons mb-2 mx-2 d-flex justify-content-start">
          <div class="input-group me-2">
            <input
              type="text"
              class="form-control filter"
              placeholder="Search for schedule"
            />
            <button class="input-group-text bg-secondary">SEARCH</button>
          </div>
          <button class="btn btn-primary">CREATE</button>
        </div>
        <div class="px-3">
          <div v-for="item in schedules" :key="item.id" class="card mb-3">
            <div class="card-body">{{ item.name }}hi</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref } from "vue";
import { Schedule } from "@/modules/schedules/types";
import { getSchedules } from "@/modules/schedules/functions";

const schedules = ref<Schedule[]>([]);

const fetchData = async () => {
  const data = await getSchedules();
  schedules.value = data;
};

fetchData();
</script>
<style lang="scss">
.main-container {
  height: 100%;
  width: 100%;
  justify-content: center;
}

.main {
  height: 100vh;
  width: 90%;
}
</style>
