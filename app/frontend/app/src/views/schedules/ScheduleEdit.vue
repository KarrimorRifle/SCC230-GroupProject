<template>
  <div class="main mx-0 d-flex">
    <div class="header">
      <h2>Name of the schedule</h2>
    </div>
    <div class="container-fluid mx-0 px-0">
      <div class="row mx-0">
        <div class="col p-3" style="max-height: 100">
          <trigger-block />
          <div
            v-for="(command, index) in commands"
            :key="index"
            style="margin-top: -0.6rem"
          >
            <block-item
              v-if="['SET', 'FOR', 'END'].includes(command)"
              :command-type="command"
              @delete="commands.splice(index, 1)"
            />
            <block-conditionals
              v-else
              :command-type="command"
              @delete="commands.splice(index, 1)"
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
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import BlockMenu from "./BlockMenu.vue";
import BlockItem from "./blocks/BlockItem.vue";
import TriggerBlock from "./blocks/TriggerBlock.vue";
import BlockConditionals from "./blocks/BlockConditionals.vue";
import { computed, ref } from "vue";
import { CommandType } from "@/modules/schedules/types";

const menu = ref<boolean>(false);

const commands = ref<CommandType[]>([]);
const blocks = ref<(typeof BlockItem)[]>();

const addNewBlock = (commandType: CommandType) => {
  commands.value.push(commandType);
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
