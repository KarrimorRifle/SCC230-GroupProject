<template>
  <div
    class="nub d-flex"
    v-if="!trigger"
    id="female-slot"
    :style="{ width: width }"
  >
    <div
      class="card px-1 border-bottom-0 rounded-bottom-0 border-end-0 rounded-end-0"
      :style="{ 'border-color': borderColor }"
    >
      <div class="card-body py-1"></div>
    </div>
    <div
      style="background-color: rgba(0, 0, 0, 0)"
      :style="{ 'border-color': borderColor }"
      class="card border-top-0 rounded-top-0"
    >
      <div class="card-body p-0 px-3"></div>
    </div>
    <div
      class="card flex-grow-1 border-bottom-0 rounded-bottom-0 border-start-0 rounded-start-0"
      :style="{ 'border-color': borderColor }"
    >
      <div class="card-body py-1"></div>
    </div>
  </div>
  <div
    id="functionCodeItem"
    class="card rounded-top-0 border-top-0 border-bottom-0"
    :style="{ 'border-color': borderColor, width: width }"
  >
    <div class="card-body p-2">
      <button
        class="p-0"
        v-if="!display"
        style="
          color: rgb(213, 29, 29);
          position: absolute;
          right: 0.2rem;
          top: -0.8rem;
          background-color: rgba(0, 0, 0, 0);
          border-style: none;
        "
        @click="$emit('delete')"
      >
        x
      </button>
      <div
        class="row d-flex"
        :class="{
          'justify-content-center': !['FOR', 'WAIT'].includes(commandType),
          'justify-content-start': ['FOR', 'WAIT'].includes(commandType),
        }"
      >
        <div
          class="px-0 d-flex align-items-start justify-content-center"
          :class="{
            'col-2': commandType == 'SET',
            'col-4': commandType == 'END',
            'col-5': ['FOR', 'WAIT'].includes(commandType),
          }"
        >
          <b class="pt-1" :style="{ color: borderColor }">{{ commandType }}</b>
        </div>
        <div class="col-7" v-if="['FOR', 'WAIT'].includes(commandType)">
          <div
            class="input-group-text"
            style="width: 5rem; height: 1.6rem"
            v-if="display"
          ></div>
          <input
            v-else
            v-model="forValue"
            class="input-group-text p-0 border-light"
            style="width: 5rem"
          />
        </div>
        <div class="col-9 px-0" v-else-if="commandType != 'END'">
          <div class="input-group" v-if="display">
            <button class="input-group-text">------------</button>
            <div class="input-group-text">=</div>
            <div
              class="input-group-text"
              type="number"
              style="width: 5rem"
            ></div>
          </div>
          <div class="input-group" v-else>
            <button
              class="input-group-text dropdown-toggle border-light"
              type="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              {{ setValue.displayVariable }}
            </button>
            <ul class="dropdown-menu dropdown-menu-dark px-2 pt-0">
              <template v-for="(device, index) in devices" :key="device.id">
                <li class="mt-2">
                  <b>{{ index + 1 }}: {{ device.name }}</b>
                </li>
                <li class="pt-0 pb-1 px-1">
                  <hr class="dropdown-divider m-0" />
                </li>
                <li v-for="key in Object.keys(device.data)" :key="key">
                  <button
                    class="dropdown-item"
                    @click="
                      setValue.variable = device.id + '.' + key;
                      setValue.displayVariable = index + 1 + ': ' + key;
                      setValue.type = device.data[key];
                    "
                  >
                    {{ key }}
                  </button>
                </li>
              </template>
              <template v-if="scheduleVars">
                <li class="mt-2">
                  <b>Schedule Vars</b>
                </li>
                <li class="pt-0 pb-1 px-1">
                  <hr class="dropdown-divider m-0" />
                </li>
                <li
                  v-for="(variable, index) in Object.keys(scheduleVars)"
                  :key="index"
                >
                  <button
                    class="dropdown-item"
                    @click="
                      setValue.variable = 'var.' + variable;
                      setValue.displayVariable = 'SCH: ' + variable;
                      setValue.type = scheduleVars[variable];
                    "
                  >
                    {{ variable }}
                  </button>
                </li>
              </template>
            </ul>
            <button
              class="input-group-text"
              style="background-color: rgba(0, 0, 0, 0)"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              {{ setValue.action }}
            </button>
            <ul
              class="dropdown-menu dropdown-menu-dark"
              style="min-width: 34px !important"
            >
              <li v-for="action in availableActions" :key="action">
                <button
                  class="dropdown-item p-0 d-flex justify-content-center"
                  @click="setValue.action = action"
                >
                  {{ action }}
                </button>
              </li>
            </ul>
            <input
              class="input-group-text border-light"
              type="number"
              style="width: 5rem"
              placeholder="00"
              :v-model="setValue.value"
              v-if="setValue.type == 'NUMBER'"
            />
            <div
              class="input-group-text border-light"
              v-if="setValue.type == 'BOOLEAN'"
            >
              <input
                class="form-check-input mt-0 border-primary"
                type="checkbox"
                :v-model="setValue.value"
              />
            </div>
            <button
              type="button"
              class="input-group-text border-light dropdown-toggle dropdown-toggle-split"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              <span class="visually-hidden">Toggle Dropdown</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="d-flex nub" id="male-slot" :style="{ width: width }">
    <div class="card border-0 px-1" style="background-color: rgba(0, 0, 0, 0)">
      <div class="card-body py-1"></div>
    </div>
    <div
      class="card rounded-0 rounded-bottom border-top-0"
      :style="{ 'border-color': borderColor }"
    >
      <div class="card-body p-0 px-3 py-1"></div>
    </div>
  </div>
  <div class="d-flex nub justify-content-center" id="add-item">
    <button
      class="d-flex align-content-center justify-content-center mt-1"
      style="background-color: rgba(0, 0, 0, 0); border-style: none"
      v-if="lastBlock"
    >
      <img
        src="@/assets/plus.svg"
        style="width: 1.3rem; height: 1.3rem"
        alt="plus"
      />
    </button>
  </div>
</template>
<script setup lang="ts">
import { CommandType, Device } from "@/modules/schedules/types";
import { defineProps, ref, defineExpose, computed } from "vue";

type CompareValue = "==" | "!=" | ">=" | "<=" | ">" | "<";
const forValue = ref<number>(2);

type setActions = "=" | "+=" | "-=" | "/=" | "*=";
const availableActions = ref<setActions[]>(["=", "+=", "-=", "/=", "*="]);
interface deviceSetValue {
  displayVariable: string;
  type: "NUMBER" | "BOOLEAN" | "ANY";
  variable: string;
  action: setActions;
  value: number | boolean;
}

const setValue = ref<deviceSetValue>({
  displayVariable: "exampleVariable",
  variable: "",
  action: "=",
  value: 2,
  type: "NUMBER",
});

const getCodeContent = (): string[] | boolean => {
  let strings: string[] = [];
  switch (props.commandType) {
    case "FOR":
    case "WAIT":
      return [forValue.value + ""];
    case "END":
      return [];
  }
};

const width = computed(() => {
  if (props.commandType == "END") return "7rem";
  else if (props.commandType == "FOR" || props.commandType == "WAIT")
    return "12rem";
  else return "28rem";
});

const props = defineProps<{
  trigger?: boolean;
  lastBlock?: boolean;
  display?: boolean;
  commandType: CommandType;
  devices?: Device[];
  scheduleVars?: Record<string, "NUMBER" | "BOOLEAN">;
  endSelectable?: boolean;
}>();

const borderColor = computed(() => {
  if (props.endSelectable || props.commandType != "END" || !props.display)
    return "white";
  return "gray";
});

defineExpose<{
  getCodeContent: string[] | boolean;
}>();
</script>
<style>
.dropdown-menu {
  width: 30px !important;
}

input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
}
</style>
