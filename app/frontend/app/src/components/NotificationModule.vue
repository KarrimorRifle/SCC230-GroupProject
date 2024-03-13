<template>
  <div class="card rounded" id="notification-card" v-if="visible">
    <button
      class="text-white btn p-1"
      id="remove-notif"
      @click="visible = false"
    >
      x
    </button>
    <div
      class="card-body text-start rounded border"
      :class="`bg-${notification.colour} border-${notification.colour}`"
      :style="{ color: textColour }"
    >
      <div class="card-title text-start">
        <b>{{ notification.title }}</b>
      </div>
      {{ notification.body }}
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, reactive, computed, defineExpose } from "vue";

const visible = ref<boolean>(false);
const notification = reactive({
  title: "I'm a notification!",
  body: "I am some sample text",
  colour: "secondary" as
    | "danger"
    | "secondary"
    | "info"
    | "warning"
    | "success"
    | "primary",
});

const textColour = computed(() =>
  ["info", "warning"].includes(notification.colour) ? "black" : "white"
);

const show = async (
  title: string,
  body: string,
  colour: "danger" | "secondary" | "info" | "warning" | "success" | "primary"
) => {
  notification.title = title;
  notification.body = body;
  notification.colour = colour;

  visible.value = true;
};

defineExpose({
  show,
});
</script>
<style>
#notification-card {
  position: absolute;
  z-index: 10;
  bottom: 1rem;
  right: 1rem;
  width: 20rem;
}

#remove-notif {
  position: absolute;
  top: -8px;
  right: 0px;
}
</style>
