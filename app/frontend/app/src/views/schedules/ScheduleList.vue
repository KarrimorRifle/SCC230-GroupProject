<template>
  <div class="main-container d-flex">
    <div class="main row bg-dark">
      <div class="col-2 options bg-gray"></div>
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
            <button class="input-group-text bg-gray">SEARCH</button>
          </div>
          <button class="btn btn-primary" @click="createSchedule()">
            CREATE
          </button>
        </div>
        <div class="px-3">
          <div
            v-for="item in schedules"
            :key="item.ScheduleID"
            class="card mb-3 bg-gray"
          >
            <div
              class="card-title mb-0 text-start p-2 d-flex justify-content-between"
            >
              <h5 class="me-2">{{ item.ScheduleName }}</h5>
              <div class="d-flex">
                <a
                  :href="'/schedules/' + item.ScheduleID"
                  class="btn btn-info me-2 btn-sm"
                  >EDIT</a
                >
                <div
                  class="p-2"
                  :class="{
                    'bg-success': item.IsActive,
                    'bg-danger': !item.IsActive,
                  }"
                  style="
                    width: 1rem;
                    height: 1rem;
                    border-radius: 50%;
                    border-width: 1px;
                    border-color: black;
                    border-style: solid;
                  "
                />
              </div>
            </div>
            <hr class="m-0" />
            <div class="card-body py-0 d-flex">
              <div class="me-3">
                <b>Rating: </b>
                <b :style="{ color: ratingToColor(item.Rating) }">
                  {{ item.Rating }} / 5
                </b>
              </div>
              <div>
                <b>Status: </b>
                <b :style="{ color: item.IsPublic ? 'orange' : 'green' }">
                  {{ item.IsPublic ? "Public" : "Private" }}
                </b>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref } from "vue";
import { Schedule, ListSchedule } from "@/modules/schedules/types";
import { getSchedules } from "@/modules/schedules/functions";
import axios from "axios";

const schedules = ref<ListSchedule[]>();

const fetchData = async () => {
  const data = await axios.get("http://localhost:5000/schedule", {
    withCredentials: true,
  });
  schedules.value = data.data;
  console.log(data);
};

const createSchedule = async () => {
  await axios.post(
    "http://localhost:5000/schedule",
    {
      ScheduleName: "test1",
      IsActive: 0,
      IsPublic: 0,
      Rating: 0,
    },
    {
      withCredentials: true,
    }
  );
  fetchData();
};

const ratingToColor = (rating: number) => {
  let value = rating - 2.5;
  let green = 255;
  let red = 255;
  if (value > 0) red -= (value / 2.5) * 255;
  else green += (value / 2.5) * 255;

  let redChr = Math.round(red).toString(16);
  if (redChr.length < 2) redChr = 0 + redChr;

  let greenChr = Math.round(green).toString(16);
  if (greenChr.length < 2) greenChr = 0 + greenChr;

  return "#" + redChr + greenChr + "00";
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
  height: 100%;
  width: 90%;
}

.bg-gray {
  background-color: rgb(35, 39, 49);
}
</style>
