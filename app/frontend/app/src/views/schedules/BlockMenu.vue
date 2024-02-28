<template>
  <div id="editor" class="main p-3 d-flex">
    <h3 class="ps-2 py-2 mb-4 bg-secondary rounded">
      <b>ADD BLOCK</b>
    </h3>
    <button
      v-for="(command, index) in conditionals"
      :key="index"
      class="mb-2 d-flex flex-column"
      style="background-color: rgba(0, 0, 0, 0); border-style: none"
      @click="blockConditionalsSelect(command)"
    >
      <block-conditionals
        :command-type="command"
        :display="true"
      />
    </button>
    <button
      v-for="(command, index) in other"
      :key="index"
      class="mb-2 d-flex flex-column"
      style="background-color: rgba(0, 0, 0, 0); border-style: none"
      @click="blockItemSelect(command)"
      :style="{
        cursor: !endAvailable && command == 'END' ? 'default' : 'pointer',
      }"
    >
      <block-item
        :command-type="command"
        :display="true"
        :end-selectable="endAvailable"
      />
    </button>
    <button class="btn btn-danger mt-5" @click="$emit('close')">CLOSE</button>
  </div>
</template>
<script setup lang="ts">
import BlockConditionals from "./blocks/BlockConditionals.vue";
import BlockItem from "./blocks/BlockItem.vue";
import TriggerBlock from "./blocks/TriggerBlock.vue";
import { ref, defineProps, defineEmits } from "vue";
import { CommandType } from "@/modules/schedules/types";

const conditionals = ref<CommandType[]>(["WHILE", "IF", "ELSE"]);

const other = ref<CommandType[]>(["SET", "FOR", "WAIT", "END"]);

const props = defineProps<{
  endAvailable: boolean;
}>();

const emit = defineEmits(["chosen", "close"]);

const blockItemSelect = (command: CommandType) => {
  if (props.endAvailable || command != "END") {
    emit("chosen", command);
  }
};

const blockConditionalsSelect = (command: CommandType) => {
  if (props.elseAvailable || command != "ELSE") {
    emit("chosen", command);
  }
};
</script>
<style>
#editor {
  background-color: rgb(81, 90, 113);
  height: 100%;
}
</style>
