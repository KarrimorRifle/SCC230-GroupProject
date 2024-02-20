<template>
  <div class="nub d-flex">
    <div
      class="card flex-grow-1 border-bottom-0 rounded-bottom-0 border-end-0 rounded-end-0"
      style="border-color: white"
    >
      <div class="card-body py-1"></div>
    </div>
    <div
      style="border-color: white; background-color: rgba(0, 0, 0, 0)"
      class="card border-top-0 rounded-top-0"
    >
      <div class="card-body p-0 px-3"></div>
    </div>
    <div
      class="card flex-grow-1 border-bottom-0 rounded-bottom-0 border-start-0 rounded-start-0"
      style="border-color: white"
    >
      <div class="card-body py-1"></div>
    </div>
  </div>
  <div
    id="functionCodeItem"
    class="card rounded-top-0 border-bottom-0 border-top-0"
    style="border-color: white"
  >
    <div class="card-body p-2">
      <div class="row">
        <div class="col-2 px-0 d-flex align-items-start justify-content-center">
          <b class="pt-1">{{ functionType }}</b>
        </div>
        <div class="col-7 px-0">
          <div class="d-flex flex-column">
            <div
              class="d-flex mb-1"
              v-for="(item, index) in conditions.conditions"
              :key="'condition' + index"
            >
              <div class="input-group">
                <input
                  type="number"
                  class="input-group-text border-light p-0"
                  style="width: 5rem"
                  v-model="item.value1"
                />
                <button
                  class="btn btn-outline-secondary text-light btn-sm"
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
                <input
                  type="number"
                  class="input-group-text border-light p-0"
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
              <div v-else-if="conditions.conditions.length > 1">
                <button
                  class="btn btn-sm btn-outline-danger px-3"
                  @click="
                    conditions.joining.splice(index - 1, 1);
                    conditions.conditions.splice(index, 1);
                  "
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
        <div class="col-3 justify-content-end px-0">
          <button
            class="btn btn-outline-success btn-sm text-light"
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
  <div class="d-flex nub justify-content-center">
    <div
      class="card rounded-0 rounded-bottom border-top-0"
      style="border-color: white"
    >
      <div class="card-body p-0 px-3 py-1"></div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { CommandType } from "@/modules/schedules/types";
import { defineProps, ref } from "vue";

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

// const getConditions(){ getCodeBlock
//   let strings = [];
//   string = conditions.value.conditions[0].value1 + conditions.value.conditions[0].compare
// }

defineProps<{
  functionType: CommandType;
}>();
</script>
<style>
#functionCodeItem {
  width: 28rem !important;
}

.nub {
  width: 28rem;
}

.dropdown-menu {
  width: 30px !important;
}
</style>
