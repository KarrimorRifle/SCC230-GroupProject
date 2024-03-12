<template>
  <div class="main mx-0" :key="'fnasfb'" v-if="schedule">
    <button
      class="btn invis-bg"
      id="ScheduleBackButton"
      @click="router.push('/schedules')"
    >
      {{ "< BACK" }}
    </button>
    <div class="header" :class="{ 'draft-color': schedule.IsDraft }">
      <h2>
        Edit Schedule
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
      <div class="container-fluid">
        <div class="row">
          <div class="col-12 col-xl-6 col-lg-5 px-0">
            <div class="input-group mb-1 px-2">
              <div class="input-group-text"><b>Name:</b></div>
              <input
                class="form-control"
                type="text"
                v-model="schedule.ScheduleName"
              />
            </div>
          </div>
          <div class="d-flex justify-content-between col px-0">
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
              <div
                class="input-group"
                v-if="!schedule.IsDraft"
                style="width: 8rem"
              >
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
            <div class="me-3">
              <button
                class="btn btn-secondary btn-sm me-2 border-3"
                @click="mode = 'VARS'"
              >
                VARS
              </button>
              <button
                class="btn btn-sm me-2 border-3"
                @click="toggleDraft()"
                :class="{
                  'btn-outline-warning text-light': !schedule.IsDraft,
                  'btn-warning': schedule.IsDraft,
                }"
              >
                {{ schedule.IsDraft ? "UNDRAFT" : "DRAFT" }}
              </button>
              <button
                class="btn btn-success btn-sm me-2 border-3 text-light"
                @click="saveSchedule"
              >
                SAVE
              </button>
              <button
                class="btn btn-danger btn-sm border-3 text-light"
                @click="deleteSchedule"
              >
                DELETE
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="container-fluid mx-0 px-0 d-flex flex-column">
      <div id="alkdas" class="row mx-0">
        <div class="col p-3 scrollable21" style="max-height: 100%">
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
              :schedule-vars="schedule?.VarDict"
              :highlight="focusedBlock == index"
              @change="
                menu = true;
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
        <div class="editor-side-bar col-xl-5 col-lg-6 col-12 px-0" v-if="menu">
          <variable-menu v-if="mode == 'VARS'" v-model="schedule.VarDict" />
          <block-menu
            v-else
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
      </div>
    </div>
  </div>
  <transition name="slide">
    <div v-if="showNotification" class="notification">
      <button
        style="
          position: absolute;
          top: -0.3rem;
          right: -0.1rem;
          background-color: rgba(0, 0, 0, 0);
          border-style: none;
          color: #000000;
        "
        @click="showNotification = false"
      >
        x
      </button>
      {{ errorMSG }}
    </div>
  </transition>
</template>
<script setup lang="ts">
import BlockMenu from "./BlockMenu.vue";
import TriggerBlock from "./blocks/TriggerBlock.vue";
import FunctionBlock from "./blocks/FunctionBlock.vue";
import VariableMenu from "./VariableMenu.vue";
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
const mode = ref<"CHANGE" | "ADD" | "VARS">("ADD");
const showNotification = ref(false);
const errorMSG = ref<string>("");

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
    codeBlock.Number = schedule.value.Code[focusedBlock.value].Number;
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
  //stringify params
  let tempSchedule = schedule.value;
  if (tempSchedule == undefined) return;
  tempSchedule.Code = tempSchedule.Code.map((item) => {
    let block = item;
    block.Params = item.Params?.map((item) => item + "");
    return block;
  });

  let lastIf = -1;
  try {
    tempSchedule.Code.forEach((item, index) => {
      if (item.CommandType == "IF" && tempSchedule) {
        lastIf = item.Number;
        tempSchedule.Code[index].LinkedCommands = [];
      }
      if (item.CommandType == "ELSE" && tempSchedule)
        if (lastIf != -1) {
          console.log(tempSchedule.Code[lastIf].LinkedCommands);
          tempSchedule.Code[lastIf].LinkedCommands?.push(index);
        } else throw new Error();
    });
  } catch (e) {
    showNotification.value = true;
    errorMSG.value = "NOT SAVED: 'IF' block must occur before 'ELSE'";
    return;
  }

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

  showNotification.value = true;
  errorMSG.value = "Schedule saved successfully!";
};

const toggleDraft = () => {
  if (!schedule.value?.IsDraft && schedule.value) {
    schedule.value.IsDraft = true;
    schedule.value.IsActive = false;
  } else {
    if (endAvailable.value) {
      showNotification.value = true;
      errorMSG.value = "All conditionals must be closed with an 'END' block";
    } else if (schedule.value) {
      let tempSchedule = schedule.value;
      if (!tempSchedule) return;
      try {
        let lastIf = -1;
        tempSchedule.Code.forEach((item, index) => {
          if (item.CommandType == "IF" && tempSchedule) {
            lastIf = item.Number;
            tempSchedule.Code[index].LinkedCommands = [];
          }
          if (item.CommandType == "ELSE" && tempSchedule)
            if (lastIf != -1) {
              console.log(tempSchedule.Code[lastIf].LinkedCommands);
              tempSchedule.Code[lastIf].LinkedCommands?.push(index);
            } else throw new Error();
        });
      } catch (e) {
        showNotification.value = true;
        errorMSG.value = "'IF' block must occur before 'ELSE'";
        return;
      }
      schedule.value.IsDraft = false;
    }
  }
};
</script>
<style>
.main {
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
</style>
