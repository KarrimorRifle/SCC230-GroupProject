<template>
  <div class="container-fluid main-schedule-variable-manager px-0">
    <button @click="console.log(modelValue)">hello</button>
    <h3>Variables</h3>
    <div class="variable-container">
      <div v-for="(value, key, index) in modelValue" :key="key + index">
        I am a variable
      </div>
    </div>
    <div class="variable-controller">
      <div class="container-fluid">
        <div class="row">
          <div class="col-10">
            <div class="input-group">
              <input
                type="text"
                class="form-control"
                placeholder="VariableName: No special chars"
                @input="removeSpecialCharacters"
              />
              <button class="btn btn-success me-2 input-group-text">ADD</button>
            </div>
          </div>
          <div class="col-2">
            <button class="btn btn-danger">CLOSE</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, watchEffect } from "vue";

const props = defineProps<{
  modelValue?: Record<string, "NUMBER" | "BOOLEAN">;
}>();

let modelValue = ref(props.modelValue);
watchEffect(() => {
  modelValue.value = props.modelValue;
});

const removeSpecialCharacters = (event: InputEvent) => {
  const target = event.target as HTMLInputElement;
  target.value = target.value.replace(/[^a-zA-Z0-9]/g, "");
};
</script>
<style>
.main-schedule-variable-manager {
  background: rgb(103, 103, 137);
  height: 100%;
  min-height: 0;
  display: flex;
  flex-direction: column;
}

.variable-container {
  height: 80%;
  min-height: 0;
  max-height: 80%;
  overflow-y: scroll;
  overflow-x: hidden;
}

.variable-controller {
  max-height: 20%;
  flex-grow: 1;
  min-height: 0;
}
</style>
