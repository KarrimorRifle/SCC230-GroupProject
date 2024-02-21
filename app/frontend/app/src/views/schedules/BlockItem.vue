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
        <div class="col-3" v-if="commandType == 'FOR'">
          <div
            class="input-group-text"
            style="width: 5rem; height: 1.6rem"
            v-if="display"
          ></div>
          <input
            v-else
            v-model="forValue"
            class="input-group-text p-0"
            style="width: 5rem"
          />
        </div>
        <div class="col-7 px-0" v-else-if="commandType != 'END'">lol</div>
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
</style>
