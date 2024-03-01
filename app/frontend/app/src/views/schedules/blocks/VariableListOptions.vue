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
      <li>
        <button class="dropdown-item">
          <!-- @click="
            item.varChosen = false;
            item.value2 = 0;
          "
          :class="{
            'disabled text-secondary': item.type != 'NUMBER',
          }" -->
          Number
        </button>
      </li>
      <li>
        <button class="dropdown-item">
          <!-- @click="
            item.varChosen = false;
            item.value2 = false;
          "
          :class="{
            'disabled text-secondary': item.type != 'BOOLEAN',
          }" -->
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
      <li v-for="key in Object.keys(device.data)" :key="key">
        <button class="dropdown-item">
          <!-- @click="
            item.value1 = device.id + '.' + key;
            item.DValue1 = index + 1 + ': ' + key;
            item.type = device.data[key];
            item.varChosen = false;
            item.value2 = device.data[key] == 'NUMBER' ? 0 : false;
          " -->
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
      <li v-for="(variable, index) in Object.keys(scheduleVars)" :key="index">
        <button class="dropdown-item">
          <!-- @click="
            item.value1 = 'var.' + variable;
            item.DValue1 = 'SCH: ' + variable;
            item.type = scheduleVars[variable];
            item.varChosen = false;
            item.value2 = scheduleVars[variable] == 'NUMBER' ? 0 : false;
          " -->
          {{ variable }}
        </button>
      </li>
    </template>
  </ul>
</template>
<script lang="ts" setup>
import { defineProps, ref, defineExpose, computed } from "vue";
import { Device } from "@/modules/schedules/types";

const props = defineProps<{
  devices?: Device[];
  scheduleVars?: Record<string, "NUMBER" | "BOOLEAN">;
  custom?: boolean;
  customList?: string[];
}>();
</script>
