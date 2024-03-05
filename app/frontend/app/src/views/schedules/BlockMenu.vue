<template>
  <div id="editor" class="main p-3 d-flex editor-side-bar">
    <h3
      class="ps-2 py-2 mb-4 rounded"
      :class="{ 'bg-success': mode == 'ADD', 'bg-warning': mode == 'CHANGE' }"
    >
      <b>{{ mode }} BLOCK</b>
    </h3>
    <button
      v-for="(command, index) in commands"
      :key="index"
      class="mb-2 d-flex flex-column p-0"
      :class="{ disabled: command == 'END' && !endAvailable }"
      :style="{
        cursor: command == 'END' && !endAvailable ? 'default' : 'pointer',
      }"
      style="background-color: rgba(0, 0, 0, 0); border-style: none"
      @click="blockConditionalsSelect(command)"
    >
      <function-block
        :command-type="command"
        :end-selectable="endAvailable"
        :display="true"
      />
    </button>
    <button class="btn btn-danger mt-5" @click="$emit('close')">CLOSE</button>
  </div>
</template>
<script setup lang="ts">
import FunctionBlock from "./blocks/FunctionBlock.vue";
import { ref, defineProps, defineEmits } from "vue";
import { CommandType } from "@/modules/schedules/types";

const props = defineProps<{
  endAvailable: boolean;
  mode: "ADD" | "CHANGE";
}>();

const commands = ref<CommandType[]>([
  "WHILE",
  "IF",
  "ELSE",
  "SET",
  "FOR",
  "WAIT",
  "END",
]);

const blockConditionalsSelect = (command: CommandType) => {
  if (props.endAvailable || command != "END") emit("chosen", command);
};

const emit = defineEmits(["chosen", "close"]);
</script>
<style>
#editor {
  background-color: rgb(81, 90, 113);
  height: 100%;
}

.editor-side-bar {
  position: sticky !important;
  top: 15.8rem;
}
</style>
