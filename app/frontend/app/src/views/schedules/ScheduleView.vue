<template>
  <div
    class="main-page-wow mx-0"
    :key="'fnasfb'"
    id="fbasjfnieabhj"
    v-if="schedule"
  >
    <button
      class="btn invis-bg"
      id="ScheduleBackButton"
      @click="router.push('/schedules?mode=public')"
    >
      {{ "< BACK" }}
    </button>
    <div class="header" :class="{ 'draft-color': schedule.IsDraft }">
      <h2>
        {{ schedule.ScheduleName }}
        <div
          v-if="schedule.IsDraft"
          class="px-2 py-1 bg-warning"
          style="
            font-size: 0.8rem;
            font-weight: 700;
            display: inline-block;
            border-radius: 2rem;
            color: black;
            position: relative;
            top: -0.5rem;
          "
        >
          DRAFT
        </div>
      </h2>
      <div class="container-fluid d-flex">
        <div class="text-light">
          <b> Author ID: {{ schedule.AuthorID }} </b>
        </div>
        <div>
          <fieldset class="star-rating me-2">
            <input
              type="radio"
              id="rating5"
              name="rating"
              value="5"
              v-model="starRating"
            />
            <label for="rating5" title="5 stars">
              {{ starRating >= 5 ? "&#9733;" : "&#9734;" }}
            </label>
            <input
              type="radio"
              id="rating4"
              name="rating"
              value="4"
              v-model="starRating"
            />
            <label for="rating4" title="4 stars">
              {{ starRating >= 4 ? "&#9733;" : "&#9734;" }}
            </label>
            <input
              type="radio"
              id="rating3"
              name="rating"
              value="3"
              v-model="starRating"
            />
            <label for="rating3" title="3 stars">
              {{ starRating >= 3 ? "&#9733;" : "&#9734;" }}
            </label>
            <input
              type="radio"
              id="rating2"
              name="rating"
              value="2"
              v-model="starRating"
            />
            <label for="rating2" title="2 stars">
              {{ starRating >= 2 ? "&#9733;" : "&#9734;" }}
            </label>
            <input
              type="radio"
              id="rating1"
              name="rating"
              value="1"
              v-model="starRating"
            />
            <label for="rating1" title="1 star">
              {{ starRating >= 1 ? "&#9733;" : "&#9734;" }}
            </label>
          </fieldset>
          <button class="btn btn-success">Submit rating</button>
        </div>
        <div style="align-items: baseline">
          <button class="btn btn-secondary" @click="cloneSchedule()">
            Clone Schedule
          </button>
        </div>
      </div>
    </div>
    <div class="container-fluid mx-0 px-0 d-flex flex-column">
      <div id="alkdas" class="row mx-0">
        <div
          class="col p-3 scrollable21 d-flex flex-column align-items-center"
          v-if="schedule"
          style="max-height: 100%"
        >
          <div class="code-cover"></div>
          <function-block
            v-model="schedule.Trigger"
            command-type="TRIGGER"
            :read-only="true"
          />
          <div
            v-for="(functionBlock, index) in schedule?.Code"
            :key="index"
            style="margin-top: -0.6rem"
          >
            <function-block
              :command-type="functionBlock.CommandType"
              @delete="schedule?.Code.splice(index, 1)"
              v-model="functionBlock.Params"
              :schedule-vars="schedule?.VarDict"
              :highlight="focusedBlock == index"
              :read-only="true"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import FunctionBlock from "./blocks/FunctionBlock.vue";
import { ref } from "vue";
import { Schedule } from "@/modules/schedules/types";
import router from "@/router";
import axios from "axios";

const schedule = ref<Schedule>();
const focusedBlock = ref<number>(-1);
const starRating = ref<number>(0);

let scheduleID = router.currentRoute.value.params.id;
const fetchSchedule = async () => {
  let data = await axios.get(
    `http://localhost:5000/schedule/public/${scheduleID}`,
    {
      withCredentials: true,
    }
  );
  schedule.value = data.data;
  console.log(data.data);
};

const cloneSchedule = async () => {
  console.log(starRating.value);
};

fetchSchedule();
</script>
<style>
.main-page-wow {
  width: 100%;
  background-color: rgb(45, 50, 64);
  flex-direction: column;
  display: flex;
  flex-grow: 1;
}

.notification {
  z-index: 3;
  position: fixed;
  right: 20px;
  bottom: 20px;
  padding: 20px;
  background-color: #9cdcff;
  color: #000000;
  border: 1px solid #2e2ab8;
  border-radius: 5px;
}

.header {
  background-color: rgb(58, 64, 81);
  position: sticky;
  min-height: 5.8rem;
  top: 3.7rem;
  z-index: 1;
}

@media (max-width: 992px) {
  .header {
    min-height: 8rem;
  }
}

div.header + div.container-fluid {
  flex-grow: 1;
}

#alkdas {
  flex-grow: 1;
}

body {
  color: white;
}

.block {
  margin-bottom: -2rem;
}

.scrollable21 {
  max-height: 83.5vh !important;
  overflow: scroll;
  overflow-x: hidden;
  z-index: 0;
}

.draft-color {
  color: rgb(226, 163, 5);
  border-color: rgb(198, 146, 14);
  border-style: solid;
  border-width: 2px;
}

#ScheduleBackButton {
  position: absolute;
  color: rgb(237, 237, 237);
  border-style: solid;
  border-color: gray;
  background-color: rgb(45, 50, 64);
  top: 4rem;
  left: 0.5rem;
  z-index: 5;
}

.code-cover {
  position: fixed;
  width: 40rem;
  height: 100%;
  background: rgba(0, 0, 0, 0);
  z-index: 4;
  top: 10rem;
}

.star-rating {
  direction: rtl;
  display: inline-block;
}

.star-rating input[type="radio"] {
  display: none;
}

.star-rating label {
  color: lightgray;
  font-size: 30px;
  cursor: pointer;
}

.star-rating input[type="radio"]:checked ~ label {
  color: gold;
}
</style>
