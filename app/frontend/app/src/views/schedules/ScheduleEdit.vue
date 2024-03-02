<template>
  <div class="main mx-0 d-flex">
    <div class="header" v-if="schedule">
      <h2>Edit Schedule</h2>
      <div class="input-group mb-1">
        <div class="input-group-text"><b>Name:</b></div>
        <input
          class="form-control"
          type="text"
          v-model="schedule.ScheduleName"
        />
      </div>
      <div class="d-flex justify-content-between">
        <div class="d-flex">
          <div class="input-group me-2" style="width: 8rem">
            <div class="input-group-text">Public?</div>
            <div class="input-group-text">
              <input
                type="checkbox"
                v-model.number="schedule.IsPublic"
                :true-value="1"
                :false-value="0"
                class="form-check-input mt-0"
              />
            </div>
          </div>
          <div class="input-group" style="width: 8rem">
            <div class="input-group-text">Active?</div>
            <div class="input-group-text">
              <input
                type="checkbox"
                v-model.number="schedule.IsActive"
                :true-value="1"
                :false-value="0"
                class="form-check-input mt-0"
              />
            </div>
          </div>
        </div>
        <div>
          <button class="btn btn-success btn-sm me-2" @click="saveSchedule">
            SAVE
          </button>
          <button class="btn btn-danger btn-sm" @click="deleteSchedule">
            DELETE
          </button>
        </div>
      </div>
    </div>
    <div class="container-fluid mx-0 px-0">
      <div class="row mx-0">
        <div class="col p-3" style="max-height: 100%">
          <trigger-block />
          <div
            v-for="(functionBlock, index) in schedule?.Code"
            :key="index"
            style="margin-top: -0.6rem"
          >
            <function-block
              :command-type="functionBlock.CommandType"
              @delete="schedule?.Code.splice(index, 1)"
              v-model="functionBlock.Params"
              :devices="validDevices"
              :schedule-vars="variables"
              :highlight="focusedBlock == index"
              @change="
                mode = 'CHANGE';
                focusedBlock = index;
              "
            />
          </div>
          <div style="width: 7rem" class="mt-1">
            <button
              style="background-color: rgba(0, 0, 0, 0); border-style: none"
              @click="
                menu = true;
                mode = 'ADD';
                focusedBlock = -1;
              "
            >
              <img
                src="../../assets/plus.svg"
                alt=""
                style="width: 1.8rem; height: 1.8rem"
              />
            </button>
          </div>
        </div>
        <div class="col-4 px-0" v-if="menu">
          <block-menu
            @close="
              menu = false;
              focusedBlock = -1;
              mode = 'ADD';
            "
            @chosen="addNewBlock"
            :mode="mode"
            :end-available="endAvailable"
          />
        </div>
        <button @click="console.log(schedule)">hi</button>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import BlockMenu from "./BlockMenu.vue";
import TriggerBlock from "./blocks/TriggerBlock.vue";
import FunctionBlock from "./blocks/FunctionBlock.vue";
import { computed, ref } from "vue";
import {
  CommandType,
  Device,
  FunctionCode,
  Schedule,
} from "@/modules/schedules/types";
import router from "@/router";
import axios from "axios";

const menu = ref<boolean>(true);
const schedule = ref<Schedule>();
const nextNum = ref<number>(0);
const focusedBlock = ref<number>(-1);
const mode = ref<"CHANGE" | "ADD">("ADD");

const addNewBlock = (commandType: CommandType) => {
  let codeBlock: FunctionCode = {
    CommandType: commandType,
    Number: nextNum.value,
    Params: [],
    LinkedCommands: [],
  };
  switch (commandType) {
    case "IF":
    case "WHILE":
      codeBlock.Params = ["", "==", "0"];
      break;
    case "SET":
      codeBlock.Params = ["", "=", "0"];
      break;
    case "FOR":
    case "WAIT":
      codeBlock.Params = ["3"];
      break;
  }
  if (mode.value == "ADD") {
    schedule.value?.Code.push(codeBlock);
    nextNum.value++;
  } else if (mode.value == "CHANGE" && schedule.value) {
    schedule.value.Code[focusedBlock.value] = codeBlock;
  }
};

const endAvailable = computed(() => {
  let conditionalsCount = 0;
  let endCount = 0;
  schedule.value?.Code.forEach((item) => {
    if (item.CommandType == "END") endCount++;
    else if (["WHILE", "IF", "ELSE", "FOR"].includes(item.CommandType))
      conditionalsCount++;
  });
  return conditionalsCount > endCount;
});

const validDevices = ref<Device[]>([
  {
    id: "nadandin",
    name: "Device1",
    isActive: true,
    data: {
      var1: "NUMBER",
      var2: "NUMBER",
      var3: "BOOLEAN",
    },
  },
  {
    id: "NANA",
    name: "Device2",
    isActive: true,
    data: {
      var1: "NUMBER",
      var2: "BOOLEAN",
      var3: "BOOLEAN",
    },
  },
]);

const variables = ref<Record<string, "NUMBER" | "BOOLEAN">>({
  test1: "BOOLEAN",
  test2: "NUMBER",
});

let scheduleID = router.currentRoute.value.params.id;
const fetchSchedule = async () => {
  let data = await axios.get(`http://localhost:5000/schedule/${scheduleID}`, {
    withCredentials: true,
  });
  schedule.value = data.data;
  console.log(data);
  console.log(schedule.value?.Code);
  if (schedule.value && data.data.Code[schedule.value.Code.length - 1])
    nextNum.value = data.data.Code[schedule.value.Code.length - 1].Number + 1;
};

fetchSchedule();

const deleteSchedule = async () => {
  try {
    await axios.delete(`http://localhost:5000/schedule/${scheduleID}`, {
      withCredentials: true,
    });
  } catch (e) {
    console.log(e);
  }
  router.push("/schedules");
};

const saveSchedule = async () => {
  let tempSchedule = schedule.value;
  if (tempSchedule == undefined) return;
  tempSchedule.Code = tempSchedule.Code.map((item) => {
    let block = item;
    block.Params = item.Params?.map((item) => item + "");
    return block;
  });
  try {
    console.log(tempSchedule);
    await axios.patch(
      `http://localhost:5000/schedule/${scheduleID}`,
      tempSchedule,
      {
        withCredentials: true,
      }
    );
  } catch (e) {
    console.log(e);
  }
};
</script>
<style>
.main {
  height: 100%;
  width: 100%;
  background-color: rgb(45, 50, 64);
  flex-direction: column;
}

.header {
  background-color: rgb(58, 64, 81);
  min-height: 8rem;
}

.container-fluid {
  height: 100%;
}

.row {
  height: 100%;
}

body {
  color: white;
}

.block {
  margin-bottom: -2rem;
}
</style>
