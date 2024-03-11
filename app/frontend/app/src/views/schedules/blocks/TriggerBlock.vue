<template>
  <div
    id="functionCodeItem"
    class="card border-bottom-0"
    style="border-color: rgba(0, 0, 0, 0); background-color: rgb(30, 69, 124)"
    :style="{ width: '28rem' }"
  >
    <div class="card-body p-2">
      <div class="row d-flex justify-content-center">
        <div class="px-0 d-flex align-items-start justify-content-center col-3">
          <b class="pt-1">TRIGGER</b>
        </div>
        <div class="col-8 px-0">
          <div class="d-flex flex-column">
            <div
              class="d-flex mb-1"
              v-for="(item, index) in code"
              :key="'condition' + index"
            >
              <div class="input-group">
                <button
                  class="input-group-text dropdown-toggle"
                  type="button"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  {{ item[0] ? parseVar(item[0]) : "-------" }}
                </button>
                <variable-list-options
                  :devices="devices"
                  :schedule-vars="scheduleVars"
                />
                <button
                  class="input-group-text invis-bg"
                  :style="{ 'border-color': borderColor }"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  {{ item[1] }}
                </button>
                <variable-list-options />
                <div
                  v-if="parseVar(item[2])"
                  class="input-group-text"
                  :style="{ 'border-color': borderColor }"
                >
                  {{ parseVar(item[2]) }}
                </div>
                <input
                  class="input-group-text"
                  :style="{ 'border-color': borderColor }"
                  type="number"
                  style="width: 5rem"
                  placeholder="00"
                  v-model.number="code[index * 4 + 2]"
                  v-else-if="getVarType(item[0]) == 'NUMBER'"
                />
                <div
                  class="input-group-text"
                  :style="{ 'border-color': borderColor }"
                  v-else-if="getVarType(item[0]) == 'BOOLEAN'"
                >
                  <input
                    class="form-check-input mt-0 border-primary"
                    type="checkbox"
                  />
                </div>
                <button
                  type="button"
                  class="input-group-text dropdown-toggle dropdown-toggle-split"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                  :class="{
                    disabled: !getVarType(item[0]),
                  }"
                  :style="{
                    'border-color': getVarType(item[0]) ? borderColor : 'gray',
                  }"
                >
                  <span class="visually-hidden">Toggle Dropdown</span>
                </button>
                <variable-list-options />
              </div>
              <template>
                <div v-if="item[3]" class="d-inline-block">
                  <button
                    class="btn btn-outline-info text-light btn-sm mb-1"
                    type="button"
                    data-bs-toggle="dropdown"
                    aria-expanded="false"
                    style="font-size: 80%"
                  >
                    {{ item[3] }}
                  </button>
                  <ul
                    class="dropdown-menu pb-0"
                    style="font-size: 80%; min-width: 3rem !important"
                  >
                    <li>
                      <button class="dropdown-item px-2">AND</button>
                    </li>
                    <li>
                      <button class="dropdown-item px-2">OR</button>
                    </li>
                    <div class="dropdown-divider mb-0"></div>
                    <li>
                      <button
                        class="dropdown-item text-danger px-0 d-flex justify-content-center py-2"
                      >
                        <img
                          src="@/assets/delete-svgrepo-com.svg"
                          alt="delete icon"
                          style="max-width: 1.5rem"
                        />
                      </button>
                    </li>
                  </ul>
                </div>
                <div v-else>
                  <button class="btn btn-sm btn-outline-danger px-2 me-2">
                    <img
                      src="@/assets/delete-svgrepo-com.svg"
                      alt="delete icon"
                      style="width: 1.2rem"
                    />
                  </button>
                </div>
              </template>
            </div>
          </div>
        </div>
        <div class="col justify-content-end px-0">
          <button
            class="btn btn-success btn-sm text-light mt-1"
            style="font-size: 80%"
          >
            +
          </button>
        </div>
      </div>
    </div>
  </div>
  <div class="d-flex nub" id="male-slot" :style="{ width: '28rem' }">
    <div class="card border-0 px-1" style="background-color: rgba(0, 0, 0, 0)">
      <div class="card-body py-1"></div>
    </div>
    <div
      class="card rounded-0 rounded-bottom border-top-0"
      style="border-color: rgba(0, 0, 0, 0); background-color: rgb(30, 69, 124)"
    >
      <div class="card-body p-0 px-3 py-1"></div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { CommandType, Device } from "@/modules/schedules/types";
import { defineProps, ref, defineExpose, computed } from "vue";

const code = ref([["1", "3", "2"]]);
const borderColor = ref<string>("white");

const props = defineProps<{
  commandType: CommandType;
  devices?: Device[];
  scheduleVars?: Record<string, "NUMBER" | "BOOLEAN">;
}>();

const parseVar = (variable: string) => {
  let varArray: string[];
  try {
    varArray = variable.split(".");
  } catch {
    return undefined;
  }
  if (varArray[0] == "var" && props.scheduleVars) return "SCH: " + varArray[1];
  else {
    let index = props.devices?.findIndex((device) => device.id == varArray[0]);
    if (index != undefined && varArray[1])
      return index + 1 + ": " + varArray[1];
  }
  return undefined;
};

const getVarType = (variable: string) => {
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

const setVarType = (type: "NUMBER" | "BOOLEAN" | undefined, index: number) => {
  if (type == "NUMBER") code.value[index * 4 + 2] = "0";
  if (type == "BOOLEAN") code.value[index * 4 + 2] = "false";
};

const trigger = ref(true);

defineExpose<{
  getCodeContent: string[] | boolean;
}>();
</script>
<style>
.dropdown-menu {
  width: 30px !important;
}
</style>
