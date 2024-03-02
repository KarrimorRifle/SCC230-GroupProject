<template>
  <div class="main mx-0 d-flex">
    <div class="header">
      <h2>Name of the schedule</h2>
    </div>
    <div class="container-fluid mx-0 px-0">
      <div class="row mx-0">
        <div class="col p-3" style="max-height: 100%">
          <trigger-block />
          <div
            v-for="(functionBlock, index) in functionCode"
            :key="index"
            style="margin-top: -0.6rem"
          >
            <function-block
              :command-type="functionBlock.CommandType"
              @delete="commands.splice(index, 1)"
              v-model="functionBlock.Params"
              :devices="validDevices"
              :schedule-vars="variables"
            />
          </div>
          <div style="width: 7rem" class="mt-1">
            <button
              style="background-color: rgba(0, 0, 0, 0); border-style: none"
              @click="menu = true"
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
            @close="menu = false"
            @chosen="addNewBlock"
            :end-available="endAvailable"
          />
        </div>
        <button @click="console.log(functionCode)">hi</button>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import BlockMenu from "./BlockMenu.vue";
import TriggerBlock from "./blocks/TriggerBlock.vue";
import FunctionBlock from "./blocks/FunctionBlock.vue";
import { computed, ref } from "vue";
import { CommandType, Device, FunctionCode } from "@/modules/schedules/types";
import router from "@/router";
import axios from "axios";

const menu = ref<boolean>(true);
const functionCode = ref<FunctionCode[]>([]);
const commands = ref<CommandType[]>([]);
const nextNum = ref<number>(0);

const addNewBlock = (commandType: CommandType) => {
  commands.value.push(commandType);
  functionCode.value.push({
    CommandType: commandType,
    Number: nextNum.value,
    Params: [],
  });
};

const endAvailable = computed(() => {
  let conditionalsCount = 0;
  let endCount = 0;
  commands.value.forEach((item) => {
    if (item == "END") endCount++;
    if (["WHILE", "IF", "ELSE", "FOR"].includes(item)) conditionalsCount++;
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
// add fetching of schedule
const fetchSchedule = async () => {
  let data = await axios.get(`http://localhost:5000/schedule/${scheduleID}`, {
    withCredentials: true,
  });
  functionCode.value = data.data.Code;
  console.log(data);
  console.log(functionCode.value);
};

//reworking code blocks

fetchSchedule();
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
  min-height: 4rem;
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
