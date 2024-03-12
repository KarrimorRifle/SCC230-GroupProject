<template>
  <div class="container-fluid main-schedule-variable-manager px-0">
    <button @click="console.log(modelValue)">hello</button>
    <h3>Variables</h3>
    <div v-if="Object.keys(modelValue).length > 0" class="variable-container">
      <div v-for="(value, key, index) in modelValue" :key="key + index">
        I am a variable
      </div>
    </div>
    <div v-else class="variable-container text-muted">
      Uh oh! Nothings here...
      <br />If this is unexpected please contact us on
      <a href="tel:+447696696969">+44 7696 696969</a>
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
                v-model="newVarName"
              />
              <button
                class="btn btn-success me-2 input-group-text"
                @click="addNewVar"
              >
                ADD
              </button>
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

const newVarName = ref<string>("");

const props = defineProps<{
  modelValue: Record<string, "NUMBER" | "BOOLEAN">;
}>();

let modelValue = ref(props.modelValue);
watchEffect(() => {
  modelValue.value = props.modelValue;
});

const removeSpecialCharacters = (event: InputEvent) => {
  const target = event.target as HTMLInputElement;
  target.value = target.value.replace(/[^a-zA-Z0-9]/g, "");
};

const addNewVar = () => {
  modelValue.value[newVarName.value] = "NUMBER";
  newVarName.value = "";
};
</script>
<style>
.main-schedule-variable-manager {
  background: rgb(85, 85, 113);
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
