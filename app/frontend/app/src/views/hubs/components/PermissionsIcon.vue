<template>
  <img
    v-if="permissionLevel == 5"
    src="@/assets/permissions/5.svg"
    alt=""
    style="max-width: 2rem"
  />
  <img
    v-else-if="permissionLevel == 4"
    src="@/assets/permissions/4.svg"
    alt=""
    style="max-width: 2rem"
  />
  <img
    v-else-if="permissionLevel == 3"
    src="@/assets/permissions/3.svg"
    alt=""
    style="max-width: 2rem"
  />
  <img
    v-else-if="permissionLevel == 2"
    src="@/assets/permissions/2.svg"
    alt=""
    style="max-width: 2rem"
  />
  <img
    v-else-if="permissionLevel == 1"
    src="@/assets/permissions/1.svg"
    alt=""
    style="max-width: 2rem"
  />
</template>
<script setup lang="ts">
import { defineProps } from "vue";

const props = defineProps<{
  permissionLevel: number;
}>();
</script>
