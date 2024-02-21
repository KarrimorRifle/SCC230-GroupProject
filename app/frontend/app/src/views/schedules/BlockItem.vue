<template>
  <div
    class="nub d-flex"
    v-if="!trigger"
    id="female-slot"
    :style="{ width: width }"
  >
    <div
      class="card px-1 border-bottom-0 rounded-bottom-0 border-end-0 rounded-end-0"
      style="border-color: white"
    >
      <div class="card-body py-1"></div>
    </div>
    <div
      style="border-color: white; background-color: rgba(0, 0, 0, 0)"
      class="card border-top-0 rounded-top-0"
    >
      <div class="card-body p-0 px-3"></div>
    </div>
    <div
      class="card flex-grow-1 border-bottom-0 rounded-bottom-0 border-start-0 rounded-start-0"
      style="border-color: white"
    >
      <div class="card-body py-1"></div>
    </div>
  </div>
  <div
    id="functionCodeItem"
    class="card rounded-top-0 border-top-0"
    :class="{ 'border-bottom-0': commandType != 'END' }"
    style="border-color: white"
    :style="{ width: width }"
  >
    <div class="card-body p-2">
      <div
        class="row d-flex"
        :class="{
          'justify-content-center': commandType != 'FOR',
          'justify-content-start': commandType == 'FOR',
        }"
      >
        <div
          class="px-0 d-flex align-items-start justify-content-center"
          :class="{
            'col-2': commandType == 'SET',
            'col-4': commandType == 'END',
            'col-5': commandType == 'FOR',
          }"
        >
          <b class="pt-1">{{ commandType }}</b>
        </div>
        <div class="col-2" v-if="commandType == 'FOR'">
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
        <div class="col-8 px-0" v-else-if="commandType != 'END'">
          <!-- <div class="input-group" v-if="display">
            <button class="input-group-text dropdown-toggle">hi</button>
            <button class="input-group-text dropdown-toggle">hello</button>
            <div class="input-group-text">=</div>
            <input class="input-group-text" type="text" style="width: 5rem" />
          </div> -->
          <div
            class="input-group"
            v-for="(item, index) in setValue"
            :key="'SET' + index"
          >
            <button class="input-group-text dropdown-toggle border-light">
              hi
            </button>
            <button class="input-group-text dropdown-toggle border-light">
              hello
            </button>
            <div class="input-group-text">=</div>
            <div
              class="input-group-text border-light"
              v-if="
                item.device != undefined &&
                typeof item.device.data[item.variable] == 'boolean'
              "
            >
              <input
                class="form-check-input mt-0 border-primary"
                type="checkbox"
              />
            </div>
            <input
              class="input-group-text border-light"
              type="number"
              style="width: 5rem"
              placeholder="00"
              v-else
            />
          </div>
        </div>
        <div
          class="col-auto justify-content-end px-0"
          v-if="commandType != 'END' && commandType != 'FOR'"
        >
          <button
            class="btn btn-outline-success btn-sm text-light"
            :class="{ disabled: display }"
            style="font-size: 80%"
          >
            +
          </button>
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
      style="border-color: white"
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

//stuff to do set
interface deviceSetValue {
  device?: Device;
  variable?: string;
  value?: number | boolean;
}

const availableDevices = ref<Device[]>([]);

// const dummyData: deviceSetValue = {
//   device: {
//     id: "fhvdssf-ajfa=-fanif",
//     name: "BIG ENERGY",
//     isActive: true,
//     data: {
//       temperature: 50,
//       on: true,
//     },
//   },
// };

const setValue = ref<deviceSetValue[]>([{}]);

const getCodeContent = (): string[] | boolean => {
  let strings: string[] = [];
  try {
    console.log("hi");
  } catch {
    return false;
  }
  return strings;
};

const width = computed(() => {
  if (props.commandType == "END") return "7rem";
  else if (props.commandType == "FOR") return "12rem";
  else return "28rem";
});

const props = defineProps<{
  trigger?: boolean;
  lastBlock?: boolean;
  display?: boolean;
  commandType: CommandType;
  devices?: Device[];
}>();

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
