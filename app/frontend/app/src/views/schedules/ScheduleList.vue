<template>
  <div class="main-container d-flex">
    <div class="main row bg-dark" style="overflow: hidden">
      <div class="col-2 options bg-gray text-light">
        <div class="container-fluid sub-nav px-0">
          <div class="row sub-nav-title">NAV</div>
          <div
            class="row sub-nav-item border-top"
            :class="{
              active: personal,
            }"
          >
            <a href="/schedules?mode=personal" class="container-fluid">
              <img
                src="@/assets/home.svg"
                alt="House"
                style="max-width: 1.5rem"
              />
              My Schedules {{ $route.query.mode == "personal" ? ">" : "" }}
            </a>
          </div>
          <div
            class="row sub-nav-item"
            :class="{
              active: $route.query.mode == 'public',
            }"
          >
            <a href="/schedules?mode=public" class="container-fluid">
              <img
                src="@/assets/earth.svg"
                alt="earth"
                style="max-width: 1.5rem"
              />
              Public Schedules
            </a>
          </div>
        </div>
      </div>
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
              v-model="filterValue"
            />
          </div>
          <button
            class="btn btn-primary"
            @click="createSchedule()"
            v-if="personal"
          >
            CREATE
          </button>
        </div>
        <div class="px-3 scrollable-list21">
          <div
            v-for="item in filteredSchedules"
            :key="item.ScheduleID"
            class="card mb-3 bg-gray"
            :class="{ 'border-draft': item.IsDraft }"
          >
            <div
              class="card-title mb-0 text-start p-2 d-flex justify-content-between"
            >
              <div class="d-flex">
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
                ></div>
                <h4 class="me-2 ms-2 mb-0">
                  Name: <b>{{ item.ScheduleName }}</b>
                  <div
                    v-if="item.IsDraft"
                    class="px-2 py-1 bg-warning"
                    style="
                      font-size: 0.8rem;
                      font-weight: 700;
                      display: inline-block;
                      border-radius: 2rem;
                      color: black;
                      position: relative;
                      top: -0.3rem;
                      left: 0.4rem;
                    "
                  >
                    DRAFT
                  </div>
                </h4>
              </div>
              <div class="d-flex me-2" v-if="personal">
                <a
                  :href="'/schedules/' + item.ScheduleID"
                  class="btn btn-info me-2 btn-sm"
                  >EDIT</a
                >
                <button
                  class="btn btn-danger btn-sm"
                  @click="deleteSchedule(item.ScheduleID)"
                >
                  DELETE
                </button>
              </div>
              <div v-else>
                <a
                  :href="'/schedule/' + item.ScheduleID"
                  class="btn btn-outline-info border-2 text-light me-2 btn-sm"
                  style="font-weight: 600"
                >
                  VIEW
                </a>
                <button
                  class="btn btn-outline-danger btn-sm text-light border-2"
                  v-if="item.info"
                  @click="item['info'] = false"
                >
                  INFO
                </button>
                <button
                  v-else
                  class="btn btn-outline-secondary btn-sm text-light border-2"
                  @click="
                    item['info'] = true;
                    getScheduleData(item.ScheduleID);
                  "
                >
                  INFO
                </button>
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
            <template v-if="item.info">
              <hr class="m-0" />
              <div class="card-body py-0">
                <div
                  v-if="item.data && Object.keys(item.data).length > 0"
                ></div>
                <div class="py-3" v-else>
                  <div class="spinner-border" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                </div>
              </div>
            </template>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, computed } from "vue";
import { ListSchedule } from "@/modules/schedules/types";
import axios from "axios";
import router from "@/router";

const schedules = ref<ListSchedule[]>([]);
const filterValue = ref<string>("");
const filteredSchedules = computed(() =>
  schedules.value.filter((item) =>
    item.ScheduleName.toLowerCase().includes(filterValue.value.toLowerCase())
  )
);

const personal = computed(
  () =>
    router.currentRoute.value.query.mode == "personal" ||
    router.currentRoute.value.query.mode == undefined
);

const fetchData = async () => {
  let data;
  if (personal.value)
    data = await axios
      .get("http://localhost:5000/schedule", {
        withCredentials: true,
      })
      .catch((e) => console.log(e));
  else if (router.currentRoute.value.query.mode == "public")
    data = await axios
      .get("http://localhost:5000/schedule/public", {
        withCredentials: true,
      })
      .catch((e) => console.log(e));

  schedules.value = data.data;
  if (!personal.value)
    schedules.value = schedules.value.map((item) => ({
      ...item,
      data: undefined,
    }));
  console.log(schedules.value);
};

const createSchedule = async () => {
  await axios.post(
    "http://localhost:5000/schedule",
    {
      ScheduleName: "Schedule " + (schedules.value?.length + 1),
    },
    {
      withCredentials: true,
    }
  );
  fetchData();
};

const deleteSchedule = async (ID: string) => {
  await axios.delete(`http://localhost:5000/schedule/${ID}`, {
    withCredentials: true,
  });
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

//public schedules functions

function delay(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

const getScheduleData = async (id: string) => {
  const data = await axios
    .get(`http://localhost:5000/schedule/public/${id}`, {
      withCredentials: true,
    })
    .catch((e) => console.log(e));

  await delay(500);

  schedules.value[schedules.value.findIndex((item) => item.ScheduleID == id)][
    "data"
  ] = data.data;

  console.log(data.data);
};
</script>
<style lang="scss">
.main-container {
  flex-grow: 1;
  width: 100%;
  justify-content: center;
  align-items: center;
  display: flex;
  flex-direction: column;
}

.main {
  width: 90%;
  flex-grow: 1;
}

.bg-gray {
  background-color: rgb(47, 55, 77);
}

.scrollable-list21 {
  max-height: 82vh;
  overflow: scroll;
  overflow-x: hidden;
}

.border-draft {
  border-style: solid;
  border-width: 2px;
  border-color: rgb(166, 132, 38);
}

.sub-nav-item {
  padding-top: 1rem;
  padding-bottom: 1rem;
  border-width: 0px;
  display: flex;
  justify-content: center;
  align-content: center;

  &.active {
    > a {
      font-weight: 800 !important;
    }

    border-top: 1px solid white !important;
    border-bottom: 1px solid white !important;
    background-color: rgba(var(--bs-dark-rgb), var(--bs-bg-opacity));
  }
}

.sub-nav-item > a {
  text-decoration: none;
  color: white;
  font-weight: 500;
  text-align: center;

  > img {
    padding-bottom: 0.2rem;
  }
}

.sub-nav-title {
  font-weight: 600;
  display: flex;
  justify-content: center;
  align-content: center;
  font-size: 1.8rem;
  // border-bottom: 1px solid white;
}
</style>
