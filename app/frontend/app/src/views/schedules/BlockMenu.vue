<template>
  <div id="editor" class="main p-3">
    <trigger-block />
    <button
      v-for="(command, index) in conditionals"
      :key="index"
      class="mb-2 d-flex flex-column"
      style="background-color: rgba(0, 0, 0, 0); border-style: none"
    >
      <block-conditionals :command-type="command" :display="true" />
    </button>
    <button
      v-for="(command, index) in other"
      :key="index"
      class="mb-2 d-flex flex-column"
      style="background-color: rgba(0, 0, 0, 0); border-style: none"
    >
      <block-item :command-type="command" :display="true" />
    </button>
  </div>
</template>
<script setup lang="ts">
import BlockConditionals from "./BlockConditionals.vue";
import BlockItem from "./BlockItem.vue";
import TriggerBlock from "./TriggerBlock.vue";
import { ref } from "vue";
import { CommandType } from "@/modules/schedules/types";

const conditionals = ref<CommandType[]>(["WHILE", "IF", "ELSE"]);

const other = ref<CommandType[]>(["SET", "FOR", "END"]);
</script>
<style>
#editor {
  background-color: rgb(81, 90, 113);
  height: 100%;
}
</style>
