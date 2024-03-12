<template>
  <template v-if="customList">
    <ul class="dropdown-menu" style="min-width: 2.5rem">
      <li v-for="item in customList" :key="item">
        <button @click="$emit('option', item)" class="dropdown-item px-2">
          {{ item }}
        </button>
      </li>
    </ul>
  </template>
  <ul class="dropdown-menu dropdown-menu-dark px-2 pt-0">
    <template v-if="custom">
      <li class="mt-2">
        <b>Custom</b>
      </li>
      <li class="pt-0 pb-1 px-1">
        <hr class="dropdown-divider m-0" />
      </li>
      <li v-if="type == 'NUMBER'">
        <button class="dropdown-item" @click="$emit('custom', 'NUMBER')">
          Number
        </button>
      </li>
      <li v-if="type == 'BOOLEAN'">
        <button class="dropdown-item" @click="$emit('custom', 'BOOLEAN')">
          Boolean
        </button>
      </li>
    </template>
    <template v-for="(device, index) in devices" :key="device.id">
      <li class="mt-2">
        <b>{{ index + 1 }}: {{ device.name }}</b>
      </li>
      <li class="pt-0 pb-1 px-1">
        <hr class="dropdown-divider m-0" />
      </li>
      <li
        v-for="key in Object.keys(device.data).filter(
          (key) =>
            type == undefined || getVarType(device.id + '.' + key) == type
        )"
        :key="key"
      >
        <button
          class="dropdown-item"
          @click="$emit('chosen', device.id + '.' + key)"
        >
          {{ key }}
        </button>
      </li>
    </template>
    <template v-if="scheduleVars && Object.keys(scheduleVars).length > 0">
      <li class="mt-2">
        <b>Schedule Vars</b>
      </li>
      <li class="pt-0 pb-1 px-1">
        <hr class="dropdown-divider m-0" />
      </li>
      <li
        v-for="(variable, index) in Object.keys(scheduleVars).filter(
          (variable) =>
            type == undefined || getVarType('var.' + variable) == type
        )"
        :key="index"
      >
        <button
          class="dropdown-item"
          @click="$emit('chosen', 'var.' + variable)"
        >
          {{ variable }}
        </button>
      </li>
    </template>
  </ul>
</template>
<script lang="ts" setup>
import { defineProps, defineEmits } from "vue";
import { Device } from "@/modules/schedules/types";

const props = defineProps<{
  devices?: Device[];
  scheduleVars?: Record<string, "NUMBER" | "BOOLEAN">;
  custom?: boolean;
  customList?: string[];
  type?: "NUMBER" | "BOOLEAN";
}>();

const getVarType = (variable: string, index?: number) => {
  let varArray = variable.split(".");
  let type;
  if (varArray[0] == "var" && props.scheduleVars)
    type = props.scheduleVars[varArray[1]];
  else {
    let device = props.devices?.find((device) => device.id == varArray[0]);
    if (device) type = device.data[varArray[1]];
  }
  return type;
};

const emit = defineEmits<{
  (e: "custom", item: "NUMBER" | "BOOLEAN"): void;
  (e: "chosen", value: string): void;
  (e: "option", item: string): void;
}>();
</script>
