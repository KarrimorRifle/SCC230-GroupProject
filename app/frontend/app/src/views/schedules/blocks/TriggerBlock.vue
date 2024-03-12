<template>
  <div
    id="functionCodeItem"
    class="card border-bottom-0"
    style="border-color: rgba(0, 0, 0, 0); background-color: rgb(30, 69, 124)"
    :style="{ width: '28rem' }"
  >
    <button @click="console.log(filteredCode)">hi</button>
    <div class="card-body p-2">
      <div class="row d-flex justify-content-center">
        <div class="px-0 d-flex align-items-start justify-content-center col-3">
          <b class="pt-1">TRIGGER</b>
        </div>
        <div class="col-8 px-0">
          <div class="d-flex flex-column">
            <div
              class="d-flex mb-1"
              v-for="(value, key) in code"
              :key="'condition' + key"
            >
              <div class="input-group">
                <button
                  class="input-group-text"
                  type="button"
                  aria-expanded="false"
                >
                  {{ key ? parseVar(key) : "-------" }}
                </button>
                <button
                  class="input-group-text invis-bg"
                  :style="{ 'border-color': borderColor }"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  {{ value[0] }}
                </button>
                <variable-list-options />
                <div
                  v-if="parseVar(value[1])"
                  class="input-group-text"
                  :style="{ 'border-color': borderColor }"
                >
                  {{ parseVar(value[1]) }}
                </div>
                <input
                  class="input-group-text"
                  :style="{ 'border-color': borderColor }"
                  type="number"
                  style="width: 5rem"
                  placeholder="00"
                  v-else-if="getVarType(key) == 'NUMBER'"
                />
                <div
                  class="input-group-text"
                  :style="{ 'border-color': borderColor }"
                  v-else-if="getVarType(key) == 'BOOLEAN'"
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
                    disabled: !getVarType(key),
                  }"
                  :style="{
                    'border-color': getVarType(key) ? borderColor : 'gray',
                  }"
                >
                  <span class="visually-hidden">Toggle Dropdown</span>
                </button>
                <variable-list-options />
              </div>
              <div v-if="value[2]" class="d-inline-block">
                <button
                  class="btn btn-outline-info text-light btn-sm mb-1"
                  type="button"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                  style="font-size: 80%"
                >
                  {{ value[2] }}
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
            </div>
          </div>
        </div>
        <div class="col justify-content-end px-0">
          <button
            class="btn btn-success btn-sm text-light mt-1"
            style="font-size: 80%"
            data-bs-toggle="dropdown"
          >
            +
          </button>
          <variable-list-options
            :devices="devices"
            :scheduleVars="scheduleVars"
            @chosen="
              (item) => {
                addCondition(item);
              }
            "
          />
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
import VariableListOptions from "./VariableListOptions.vue";
import {
  defineProps,
  defineEmits,
  ref,
  defineExpose,
  computed,
  watchEffect,
} from "vue";

const code = ref<Record<string, string[]>>({});
const borderColor = ref<string>("white");
const emit = defineEmits(["update:modelValue"]);

const filteredCode = computed(() => {
  let tempObject: Record<string, string[][]> = {};
  Object.keys(code.value).forEach((key) => {
    tempObject[key] = [];
    let numOfItems = Math.ceil(code.value[key].length / 3);
    for (let index = 0; index < numOfItems; index++)
      tempObject[key][index] = code.value[key].slice(index * 3, index * 3 + 3);
  });
  // console.log(tempObject);
  return tempObject;
});

const props = defineProps<{
  modelValue?: Record<string, string[]>;
  devices?: Device[];
  scheduleVars?: Record<string, "NUMBER" | "BOOLEAN">;
}>();

watchEffect(() => {
  if (props.modelValue) {
    code.value = props.modelValue;
  }
});

// const updateCode = (index: number, newValue: string) => {
//   code.value[index] = newValue;
//   emit("update:modelValue", code.value);
// };

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

const addCondition = (item: string) => {
  if (code.value[item] == undefined) code.value[item] = ["==", "0"];
  else code.value[item].push("AND", "==", "2");
  console.log(code.value);
};

const getCode = () => {
  console.log(props.modelValue);
};
getCode();

defineExpose({
  code,
  // updateCode,
});
</script>
<style>
.dropdown-menu {
  width: 30px !important;
}
</style>
