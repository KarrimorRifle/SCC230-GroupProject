<template>
  <div class="nub d-flex" :style="{ width: '29rem' }">
    <div
      class="card px-1 border-bottom-0 rounded-bottom-0 border-end-0 rounded-end-0"
      :style="{ 'border-color': borderColor }"
    >
      <div class="card-body py-1"></div>
    </div>
    <div
      :style="{ 'border-color': borderColor }"
      class="card border-top-0 rounded-top-0 invis-bg"
    >
      <div class="card-body p-0 px-3"></div>
    </div>
    <div
      class="card flex-grow-1 border-bottom-0 rounded-bottom-0 border-start-0 rounded-start-0"
      :style="{ 'border-color': borderColor }"
    >
      <div class="card-body py-1"></div>
    </div>
  </div>
  <div
    id="functionCodeItem"
    class="card rounded-top-0 border-top-0 border-bottom-0"
    :style="{ 'border-color': borderColor, width: '29rem' }"
  >
    <button
      class="p-0 invis-bg"
      id="DELETE"
      v-if="!display"
      @click="$emit('delete')"
    >
      x
    </button>
    <div class="card-body p-2">
      <div class="row d-flex justify-content-center">
        <div
          class="col-2 px-0 d-flex align-items-start justify-content-center col-2"
        >
          <b class="pt-1" :style="{ color: borderColor }">{{ commandType }}</b>
        </div>
        <div class="col-9 px-0">
          <div class="d-flex flex-column">
            <div class="input-group" v-if="display">
              <div class="input-group-text p-0" style="width: 5rem"></div>
              <button
                class="btn btn-outline-secondary text-light btn-sm"
                :class="{ disabled: display }"
                type="button"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
                ==
              </button>
              <div class="input-group-text p-0" style="width: 5rem"></div>
            </div>
            <div
              class="d-flex mb-1"
              v-else
              v-for="(item, index) in conditions.conditions"
              :key="'condition' + index"
            >
              <div class="input-group">
                <button
                  class="input-group-text dropdown-toggle border-light"
                  type="button"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  {{ item.DValue1 ?? item.value1 ?? "-------" }}
                </button>
                <variable-list-options
                  :devices="devices"
                  :schedule-vars="scheduleVars"
                />
                <button
                  class="input-group-text invis-bg"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  {{ item.compare }}
                </button>
                <variable-list-options
                  :custom-list="['==', '!=', '>=', '<=', '>', '<']"
                />
                <div
                  v-if="item.varChosen"
                  class="input-group-text border-light"
                >
                  {{ item.DValue2 ?? item.value2 }}
                </div>
                <input
                  class="input-group-text border-light"
                  type="number"
                  style="width: 5rem"
                  placeholder="00"
                  :v-model="item.value2"
                  v-else-if="item.type == 'NUMBER'"
                />
                <div
                  class="input-group-text border-light"
                  v-else-if="item.type == 'BOOLEAN'"
                >
                  <input
                    class="form-check-input mt-0 border-primary"
                    type="checkbox"
                    :v-model="item.value2"
                  />
                </div>
                <button
                  type="button"
                  class="input-group-text border-light dropdown-toggle dropdown-toggle-split"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  <span class="visually-hidden">Toggle Dropdown</span>
                </button>
                <variable-list-options
                  :devices="devices"
                  :schedule-vars="scheduleVars"
                  :custom="true"
                />
              </div>
              <div v-if="conditions.joining[index]" class="d-inline-block">
                <button
                  class="btn btn-outline-info text-light btn-sm mb-1"
                  type="button"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                  style="font-size: 80%"
                >
                  {{ conditions.joining[index] }}
                </button>
                <ul
                  class="dropdown-menu pb-0"
                  style="font-size: 80%; min-width: 3rem !important"
                >
                  <li>
                    <button
                      @click="conditions.joining[index] = 'AND'"
                      class="dropdown-item px-2"
                    >
                      AND
                    </button>
                  </li>
                  <li>
                    <button
                      @click="conditions.joining[index] = 'OR'"
                      class="dropdown-item px-2"
                    >
                      OR
                    </button>
                  </li>
                  <div
                    class="dropdown-divider mb-0"
                    v-if="conditions.conditions.length > 1"
                  ></div>
                  <li>
                    <button
                      class="dropdown-item text-danger px-0 d-flex justify-content-center py-2"
                      @click="
                        conditions.joining.splice(index, 1);
                        conditions.conditions.splice(index, 1);
                      "
                      v-if="conditions.conditions.length > 1"
                    >
                      <img
                        src="@/assets/delete-svgrepo-com.svg"
                        alt="delete icon"
                        style="max-width: 1.5rem"
                      />
                    </button>
                  </li>
                </ul>
              </div>
              <div
                v-else-if="
                  conditions.conditions.length > 1 || commandType == 'ELSE'
                "
              >
                <button
                  class="btn btn-sm btn-outline-danger px-2 me-2"
                  @click="
                    conditions.joining.splice(index - 1, 1);
                    conditions.conditions.splice(index, 1);
                  "
                  :class="{ disabled: display }"
                >
                  <img
                    src="@/assets/delete-svgrepo-com.svg"
                    alt="delete icon"
                    style="width: 1.2rem"
                  />
                </button>
              </div>
            </div>
          </div>
        </div>
        <div class="col justify-content-end px-0">
          <button
            class="btn btn-success btn-sm text-light"
            :class="{ disabled: display }"
            style="font-size: 80%"
            @click="addCondition"
          >
            +
          </button>
        </div>
      </div>
    </div>
  </div>
  <div class="d-flex nub" :style="{ width: '29rem' }">
    <div class="card border-0 px-1 invis-bg">
      <div class="card-body py-1"></div>
    </div>
    <div
      class="card rounded-0 rounded-bottom border-top-0"
      :style="{ 'border-color': borderColor }"
    >
      <div class="card-body p-0 px-3 py-1"></div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { CommandType, Device } from "@/modules/schedules/types";
import { defineProps, ref, defineExpose, computed } from "vue";
import VariableListOptions from "./VariableListOptions.vue";

const props = defineProps<{
  display?: boolean;
  commandType: CommandType;
  devices?: Device[];
  scheduleVars?: Record<string, "NUMBER" | "BOOLEAN">;
}>();

type CompareValue = "==" | "!=" | ">=" | "<=" | ">" | "<";
type Joining = "AND" | "OR";
interface Condition {
  value1: string | undefined;
  DValue1?: string;
  type: "NUMBER" | "BOOLEAN";
  compare: CompareValue;
  value2: number | string | boolean | undefined;
  DValue2?: string;
  varChosen: boolean;
}

const borderColor = computed(() => "WHITE");

const getCodeContent = (): string[] | boolean => {
  let strings: string[] = [];
  try {
    conditions.value.conditions.forEach((item, index) => {
      if (item.value1 == undefined || item.value2 == undefined)
        throw new Error("INVALID");
      strings.push(item.value1 + "");
      strings.push(item.compare);
      strings.push(item.value2 + "");
      if (conditions.value.joining[index])
        strings.push(conditions.value.joining[index]);
    });
  } catch {
    return false;
  }
  return strings;
};

const conditions = ref<{ conditions: Condition[]; joining: Joining[] }>({
  conditions:
    props.commandType != "ELSE"
      ? [
          {
            value1: undefined,
            compare: "==",
            value2: undefined,
            type: "NUMBER",
            varChosen: false,
          },
        ]
      : [],
  joining: [],
});

const addCondition = () => {
  conditions.value.conditions.push({
    value1: undefined,
    compare: "==",
    value2: undefined,
    type: "NUMBER",
    varChosen: false,
  });
  if (conditions.value.conditions.length > 1)
    conditions.value.joining.push("AND");
};

defineExpose<{
  getCodeContent: string[] | boolean;
}>();
</script>
<style>
.dropdown-menu {
  width: 30px !important;
}

#DELETE {
  color: rgb(213, 29, 29);
  position: absolute;
  right: 0.2rem;
  top: -0.8rem;
  border-style: none;
}

.invis-bg {
  background-color: rgba(0, 0, 0, 0);
}
</style>
