<template>
  <nav
    class="navbar navbar-expand-lg bg-body-tertiary px-3"
    data-bs-theme="dark"
  >
    <div class="container-fluid">
      <a class="navbar-brand" href="#">
        <img
          src="../assets/gear-svgrepo-com.svg"
          style="max-height: 2rem"
          alt=""
        />
      </a>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <a
              class="nav-link text-light"
              :class="{ active: route.path == '/' }"
              aria-current="page"
              href="/"
              >Home</a
            >
          </li>
          <li class="nav-item">
            <a class="nav-link text-light" href="#">Link</a>
          </li>
          <li class="nav-item">
            <a class="nav-link text-light" aria-disabled="true">Disabled</a>
          </li>
        </ul>
        <div v-if="!loggedIn" class="d-flex justify-content-center">
          <div class="nav-item me-3">
            <a
              class="nav-link text-secondary"
              href="/signup"
              :class="{ 'active text-light': route.path == '/signup' }"
            >
              Sign up
            </a>
          </div>
          <div class="nav-item">
            <a
              class="nav-link text-light"
              href="/login"
              :class="{ active: route.path == '/login' }"
            >
              Log in
            </a>
          </div>
        </div>
        <div v-else>
          <div class="nav-item">
            <a
              class="nav-link text-light"
              href="/account"
              :class="{ active: route.path == '/account' }"
            >
              Account
            </a>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script lang="ts" setup>
import { useRoute } from "vue-router";
import { getCookies } from "@/functions";
let loggedIn = false;

const route = useRoute();
if (getCookies()["session_id"] != null) loggedIn = true;
</script>

<style>
.active {
  font-weight: 600 !important;
}
</style>
