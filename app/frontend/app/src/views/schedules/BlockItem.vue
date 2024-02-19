<template>
  <div id="functionCodeItem" class="card border-0">
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
</template>
<script setup lang="ts">
import { CommandType } from "@/modules/schedules/types";
import { BIconCloudDownloadFill } from "bootstrap-vue";
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

.dropdown-menu {
  width: 30px !important;
}
</style>
