<template>
  <div id="editor" class="main p-3">
    <button
      v-for="(command, index) in commandType"
      :key="index"
      class="mb-2"
      style="background-color: rgba(0, 0, 0, 0); border-style: none"
    >
      <block-item :command-type="command" :display="true" />
    </button>
  </div>
</template>
<script setup lang="ts">
import BlockItem from "./BlockItem.vue";
import { ref } from "vue";
import { CommandType } from "@/modules/schedules/types";

const commandType = ref<CommandType[]>([
  "FOR",
  "WHILE",
  "IF",
  "ELSE",
  "SET",
  "GET",
  "END",
]);
</script>
<style>
#editor {
  background-color: rgb(81, 90, 113);
  height: 100%;
}
</style>
