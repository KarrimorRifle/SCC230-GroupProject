<template>
  <div>
    Lorem ipsum dolor sit amet consectetur adipisicing elit. Quis in voluptatum
    reiciendis consequatur numquam quas quibusdam, qui molestias possimus
    officiis aspernatur nam modi, consequuntur sed adipisci dolorum ratione eius
    architecto. Inventore ipsum quae assumenda quas officia quis in. Iste
    debitis reprehenderit nihil perspiciatis accusamus ad ut quo velit dolorem
    vel aliquam dolores, ullam a fuga earum minima deleniti officiis. Maxime.
    Voluptatibus labore reprehenderit voluptates iusto vitae repudiandae et nam
    officia in voluptatem, esse distinctio perferendis amet expedita cum odio
    odit fuga sint libero! Aspernatur, porro dolor nemo nihil aliquam animi.
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import axios from "axios";

const hubsList = ref<

const setup = async () => {
  let data = await axios.get("http://localhost:5000/hub", {
    withCredentials: true,
  });
  console.log(data.data);
};

setup();
</script>
