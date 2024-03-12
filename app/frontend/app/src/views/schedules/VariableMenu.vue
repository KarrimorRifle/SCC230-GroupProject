<template>
  <div class="container-fluid main-schedule-variable-manager px-0">
    <h3>Variables</h3>
    <div v-if="Object.keys(modelValue).length > 0" class="variable-container">
      <table id="varTable" class="container-fluid">
        <tr class="mb-3 stick-top">
          <th>Variable Name</th>
          <th>Value Type</th>
          <th></th>
        </tr>
        <tr v-for="(value, key, index) in modelValue" :key="key + index">
          <td>{{ key }}</td>
          <td class="input-group">
            <button
              class="btn dropdown-toggle container-fluid btn-secondary py-1 rounded-0 invis-bg border-0"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              {{ value }}
            </button>
            <ul class="dropdown-menu">
              <li>
                <button
                  class="dropdown-item variable-chooser"
                  @click="modelValue[key] = 'NUMBER'"
                >
                  NUMBER
                </button>
              </li>
              <li>
                <button
                  class="dropdown-item"
                  @click="modelValue[key] = 'BOOLEAN'"
                >
                  BOOLEAN
                </button>
              </li>
            </ul>
          </td>
          <td>
            <button class="border-0 invis-bg" @click="delete modelValue[key]">
              <img
                src="@/assets/delete-svgrepo-com.svg"
                alt="DELETE"
                class="px-1"
                style="min-width: 1.5rem; max-width: 2rem"
              />
            </button>
          </td>
        </tr>
      </table>
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
            <div
              class="validity-feedback border border-2 border-danger rounded bg-secondary"
              v-if="invalid"
            >
              Variable is invalid or already exists, pick another name
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
const invalid = ref<boolean>(false);

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
  if (
    newVarName.value == "" ||
    Object.keys(modelValue.value).includes(newVarName.value)
  ) {
    invalid.value = true;
    return;
  }

  modelValue.value[newVarName.value] = "NUMBER";
  newVarName.value = "";
  invalid.value = false;
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
  flex-grow: 8;
  overflow-y: scroll;
  overflow-x: hidden;
  max-height: 65vh;
}

.variable-controller {
  max-height: 20%;
  flex-grow: 1;
  min-height: 0;
}

.variable-chooser:hover {
  background-color: rgba(0, 0, 0, 0);
}

#varTable > tr {
  /* border-bottom: 1px; */
  border-style: solid;
  border-color: white;
}

table#varTable tr:nth-child(2n) {
  background-color: rgb(113, 112, 146);
}

table#varTable tr:nth-child(n + 1) > td:first-child {
  width: 60%;
  padding-left: 2rem;
  text-align: start;
  border-right: 2px;
  border-style: solid;
  border-color: rgba(255, 255, 255, 0.486);
}
</style>
