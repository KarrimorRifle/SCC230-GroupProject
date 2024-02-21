<template>
  <div
    id="functionCodeItem"
    class="card border-bottom-0"
    style="border-color: rgba(0, 0, 0, 0); background-color: rgb(25, 58, 104)"
    :style="{ width: '28rem' }"
  >
    <div class="card-body p-2">
      <div class="row d-flex justify-content-center">
        <div
          class="col-2 px-0 d-flex align-items-start justify-content-center col-2"
          style="font-size: 90%"
        >
          <b class="pt-1">TRIGGER</b>
        </div>
        <div class="col-7 px-0">
          <div class="d-flex flex-column">
            <div
              class="d-flex mb-1"
              v-for="(item, index) in conditions.conditions"
              :key="'condition' + index"
            >
              <div class="input-group">
                <div
                  v-if="display"
                  class="input-group-text p-0"
                  style="width: 5rem"
                ></div>
                <input
                  v-else
                  type="number"
                  class="input-group-text border-light p-0"
                  :class="{ disabled: display }"
                  style="width: 5rem"
                  v-model="item.value1"
                />
                <button
                  class="btn btn-outline-secondary text-light btn-sm"
                  :class="{ disabled: display }"
                  type="button"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  {{ item.compare }}
                </button>
                <ul class="dropdown-menu" style="min-width: 2.5rem">
                  <li>
                    <button
                      @click="item.compare = '=='"
                      class="dropdown-item px-2"
                    >
                      {{ "==" }}
                    </button>
                  </li>
                  <li>
                    <button
                      @click="item.compare = '!='"
                      class="dropdown-item px-2"
                    >
                      {{ "!=" }}
                    </button>
                  </li>
                  <li>
                    <button
                      @click="item.compare = '>='"
                      class="dropdown-item px-2"
                    >
                      {{ ">=" }}
                    </button>
                  </li>
                  <li>
                    <button
                      @click="item.compare = '<='"
                      class="dropdown-item px-2"
                    >
                      {{ "<=" }}
                    </button>
                  </li>
                  <li>
                    <button
                      @click="item.compare = '>'"
                      class="dropdown-item px-2"
                    >
                      {{ ">" }}
                    </button>
                  </li>
                  <li>
                    <button
                      @click="item.compare = '<'"
                      class="dropdown-item px-1"
                    >
                      {{ "<" }}
                    </button>
                  </li>
                </ul>
                <div
                  v-if="display"
                  class="input-group-text p-0"
                  style="width: 5rem"
                ></div>
                <input
                  v-else
                  type="number"
                  class="input-group-text border-light p-0"
                  :class="{ disabled: display }"
                  style="width: 5rem"
                  v-model="item.value2"
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
                        src="../../assets/delete-svgrepo-com.svg"
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
                    src="../../assets/delete-svgrepo-com.svg"
                    alt="delete icon"
                    style="width: 1.2rem"
                  />
                </button>
              </div>
            </div>
          </div>
        </div>
        <div class="col-auto justify-content-end px-0">
          <button
            class="btn btn-outline-success btn-sm text-light"
            :class="{ disabled: display }"
            style="font-size: 80%"
            @click="
              conditions.conditions.push({
                value1: undefined,
                compare: '==',
                value2: undefined,
              });
              conditions.joining.push('AND');
            "
          >
            + condition
          </button>
        </div>
      </div>
    </div>
  </div>
  <div class="d-flex nub" id="male-slot" :style="{ width: '28rem' }">
    <div class="card border-0 px-1" style="background-color: rgba(0, 0, 0, 0)">
      <div class="card-body py-1"></div>
    </div>
    <div
      class="card rounded-0 rounded-bottom border-top-0"
      style="border-color: rgba(0, 0, 0, 0); background-color: rgb(25, 58, 104)"
    >
      <div class="card-body p-0 px-3 py-1"></div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { CommandType } from "@/modules/schedules/types";
import { defineProps, ref, defineExpose, computed } from "vue";

type CompareValue = "==" | "!=" | ">=" | "<=" | ">" | "<";
// const compare = ref<CompareValue>("==");

interface Condition {
  value1: number | undefined;
  compare: CompareValue;
  value2: number | undefined;
}

type Joining = "AND" | "OR";

const conditions = ref<{ conditions: Condition[]; joining: Joining[] }>({
  conditions: [{ value1: undefined, compare: "==", value2: undefined }],
  joining: [],
});

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

const trigger = ref(true);

defineExpose<{
  getCodeContent: string[] | boolean;
}>();
</script>
<style>
.dropdown-menu {
  width: 30px !important;
}
</style>
