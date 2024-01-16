<script setup lang="ts">
import NavBar from "@/components/NavBar.vue";
import "bootstrap";
</script>
<template style="background-color: rgb(240, 240, 240)">
  <div
    data-bs-theme="dark"
    style="
      min-height: 100vh;
      height: 100%;
      width: 100%;
      background: rgb(63, 94, 251);
      background: radial-gradient(
        circle,
        rgb(3, 132, 212) 0%,
        rgb(7, 44, 103) 100%
      );
    "
  >
    <nav-bar />
    <router-view />
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
