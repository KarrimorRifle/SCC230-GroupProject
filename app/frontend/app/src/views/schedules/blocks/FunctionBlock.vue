<template>
  <div
    class="nub d-flex"
    v-if="commandType != 'TRIGGER'"
    :style="{ width: width }"
  >
    <div
      class="card px-1 border-bottom-0 rounded-bottom-0 border-end-0 rounded-end-0"
      :style="{ 'border-color': borderColor }"
    >
      <div class="card-body py-1"></div>
    </div>
    <div
      :style="{ 'border-color': borderColor }"
      class="card border-top-0 rounded-top-0 invis-bg"
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
    class="card border-bottom-0"
    :class="{
      'rounded-top-0 border-top-0': commandType != 'TRIGGER',
    }"
    :style="{
      'border-color': borderColor,
      width: width,
      'background-color': `${
        commandType == 'TRIGGER' ? 'rgb(30, 69, 124)' : ''
      }`,
    }"
  >
    <template v-if="commandType != 'TRIGGER'">
      <button
        class="p-0 invis-bg"
        id="DELETE"
        v-if="!display"
        @click="$emit('delete')"
      >
        x
      </button>
      <button
        class="p-0 invis-bg"
        id="CHANGE"
        v-if="!display"
        @click="$emit('change')"
      >
        ...
      </button>
    </template>
    <div class="card-body p-2">
      <div class="row d-flex justify-content-center">
        <div
          class="px-0 d-flex align-items-start justify-content-center"
          :class="{
            'col-2': commandType != 'TRIGGER',
            'col-3': commandType == 'TRIGGER',
          }"
        >
          <b class="pt-1" :style="{ color: borderColor }">{{ commandType }}</b>
        </div>
        <template v-if="commandType != 'END'">
          <div class="col-7 ms-2" v-if="['FOR', 'WAIT'].includes(commandType)">
            <div
              class="input-group-text"
              style="width: 5rem; height: 1.6rem"
              v-if="display"
            ></div>
            <input
              v-else
              class="input-group-text p-0"
              style="width: 5rem"
              :style="{ 'border-color': borderColor }"
              placeholder="00"
              v-model.number="code[0]"
            />
          </div>
          <div
            v-else
            class="px-0"
            :class="{
              'col-9': commandType != 'TRIGGER',
              'col-8': commandType == 'TRIGGER',
            }"
          >
            <div class="d-flex flex-column">
              <div class="input-group" v-if="display">
                <div class="input-group-text p-0" style="width: 5rem"></div>
                <button
                  class="btn btn-outline-secondary text-light btn-sm"
                  :class="{ disabled: display }"
                  type="button"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  {{ list[0] }}
                </button>
                <div class="input-group-text p-0" style="width: 5rem"></div>
              </div>
              <div
                class="d-flex mb-1"
                v-else
                v-for="(item, index) in filteredCode"
                :key="'condition' + index + item[1]"
              >
                <div class="input-group">
                  <button
                    class="input-group-text dropdown-toggle"
                    :style="{ 'border-color': borderColor }"
                    type="button"
                    data-bs-toggle="dropdown"
                    aria-expanded="false"
                  >
                    {{ item[0] ? parseVar(item[0]) : "-------" }}
                  </button>
                  <variable-list-options
                    v-if="!readOnly"
                    :devices="devices"
                    :schedule-vars="scheduleVars"
                    @chosen="
                      (value) => {
                        code[index * 4] = value;
                        setVarType(getVarType(item[0]), index);
                      }
                    "
                  />
                  <button
                    class="input-group-text invis-bg"
                    :style="{ 'border-color': borderColor }"
                    data-bs-toggle="dropdown"
                    aria-expanded="false"
                  >
                    {{ item[1] }}
                  </button>
                  <variable-list-options
                    v-if="!readOnly"
                    :custom-list="
                      getVarType(item[0]) == 'BOOLEAN' ? list.slice(0, 2) : list
                    "
                    @option="
                      (item) => {
                        code[index * 4 + 1] = item;
                      }
                    "
                  />
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
                      v-model="code[index * 4 + 2]"
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
                      'border-color': getVarType(item[0])
                        ? borderColor
                        : 'gray',
                    }"
                  >
                    <span class="visually-hidden">Toggle Dropdown</span>
                  </button>
                  <variable-list-options
                    :devices="devices"
                    :schedule-vars="scheduleVars"
                    :custom="true"
                    :type="getVarType(item[0])"
                    v-if="getVarType(item[0]) && !readOnly"
                    @chosen="(value) => (code[index * 4 + 2] = value)"
                    @custom="(type) => setVarType(type, index)"
                  />
                </div>
                <template
                  v-if="filteredCode.length > 1 || commandType == 'ELSE'"
                >
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
                        <button
                          class="dropdown-item px-2"
                          @click="code[index * 4 + 3] = 'AND'"
                        >
                          AND
                        </button>
                      </li>
                      <li>
                        <button
                          class="dropdown-item px-2"
                          @click="code[index * 4 + 3] = 'OR'"
                        >
                          OR
                        </button>
                      </li>
                      <div class="dropdown-divider mb-0"></div>
                      <li>
                        <button
                          class="dropdown-item text-danger px-0 d-flex justify-content-center py-2"
                          @click="code.splice(index * 4, 4)"
                          v-if="filteredCode.length > 1"
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
                    <button
                      class="btn btn-sm btn-outline-danger px-2 me-2"
                      @click="code.splice(index * 4 - 1, 4)"
                      :class="{ disabled: display }"
                    >
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
          <div
            class="col justify-content-end px-0"
            v-if="conditionals.includes(commandType)"
          >
            <button
              class="btn btn-success btn-sm text-light mt-1"
              :class="{ disabled: display }"
              @click="
                if (filteredCode.length > 0) code.push('AND', '', '==', '0');
                else code.push('', '==', '0');
              "
              style="font-size: 80%"
            >
              +
            </button>
          </div>
        </template>
      </div>
    </div>
  </div>
  <div class="d-flex nub" :style="{ width: width }">
    <div class="card border-0 px-1 invis-bg">
      <div class="card-body py-1"></div>
    </div>
    <div
      class="card rounded-0 rounded-bottom border-top-0"
      :style="{
        'border-color': borderColor,
        'background-color': `${
          commandType == 'TRIGGER' ? 'rgb(30, 69, 124)' : ''
        }`,
      }"
    >
      <div class="card-body p-0 px-3 py-1"></div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { CommandType, Device } from "@/modules/schedules/types";
import {
  defineProps,
  ref,
  defineExpose,
  computed,
  watchEffect,
  defineEmits,
} from "vue";
import VariableListOptions from "./VariableListOptions.vue";

const props = defineProps<{
  modelValue?: string[];
  display?: boolean;
  commandType: CommandType;
  devices?: Device[];
  scheduleVars?: Record<string, "NUMBER" | "BOOLEAN">;
  endSelectable?: boolean;
  highlight?: boolean;
  readOnly?: boolean;
}>();

const emit = defineEmits(["update:modelValue", "delete", "change"]);

const list = computed(() => {
  if (props.commandType != "SET") return ["==", "!=", ">=", "<=", ">", "<"];
  return ["=", "+=", "-=", "/=", "*="];
});

const conditionals = ref<CommandType[]>(["WHILE", "IF", "ELSE", "TRIGGER"]);
const code = ref<string[]>(props.modelValue || ["", list.value[0], ""]);

watchEffect(() => {
  if (props.modelValue) {
    code.value = props.modelValue;
    if (code.value.length < 2) code.value = ["", "==", "0"];
  }
});

const updateCode = (index: number, newValue: string) => {
  code.value[index] = newValue;
  emit("update:modelValue", code.value);
};

const filteredCode = computed(() => {
  let remainingArray = code.value;
  let splitArrays = [];
  while (remainingArray.length > 0) {
    splitArrays.push(remainingArray.slice(0, 4));
    remainingArray = remainingArray.slice(4);
  }
  return splitArrays;
});

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

const parseVar = (variable: string) => {
  let varArray: string[];
  try {
    varArray = variable.split(".");
  } catch {
    return undefined;
  }
  if (varArray[0] == "var" && props.scheduleVars)
    if (Object.keys(props.scheduleVars).includes(varArray[1]))
      return "SCH: " + varArray[1];
    else return;
  else {
    let index = props.devices?.findIndex((device) => device.id == varArray[0]);
    if (index != undefined && varArray[1])
      return index + 1 + ": " + varArray[1];
  }
  return undefined;
};

const borderColor = computed(() => {
  if (props.highlight) return "orange";
  if (props.endSelectable || props.commandType != "END" || !props.display)
    return "white";
  return "gray";
});

const width = computed(() => {
  switch (props.commandType) {
    case "END":
      return "7rem";
    case "WAIT":
    case "FOR":
      return "12rem";
    case "SET":
      return "28rem";
    default:
      return "29rem";
  }
});

// const getCode = () => {
//   console.log(props.modelValue);
// };
// getCode();

defineExpose({
  code,
  updateCode,
});
</script>
<style>
.dropdown-menu {
  width: 30px !important;
}

#DELETE {
  color: rgb(213, 29, 29);
  position: absolute;
  right: 0.2rem;
  top: -0.8rem;
  border-style: none;
}

#CHANGE {
  color: rgb(192, 192, 192);
  position: absolute;
  right: 1rem;
  top: -0.8rem;
  border-style: none;
}

.invis-bg {
  background-color: rgba(0, 0, 0, 0);
}
</style>
