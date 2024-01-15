<template>
  <div
    class="d-flex align-items-start justify-content-center"
    style="height: 90vh"
    data-bs-theme="dark"
  >
    <div
      class="card"
      style="width: 35%; margin-top: 6rem; height: 23rem; padding-top: 1rem"
    >
      <form action="" class="p-3 pt-0 pb-0 card-body">
        <div style="min-height: 1.3rem" class="form-text text-warning">
          {{ error }}
        </div>
        <div class="mb-3">
          <label
            for="exampleInputEmail1"
            class="form-label text-start ps-2"
            style="width: 100%"
            ><b>Email address</b></label
          >
          <input
            type="email"
            class="form-control"
            id="exampleInputEmail1"
            v-model="email"
          />
        </div>
        <div class="mb-3">
          <label
            for="exampleInputPassword1"
            class="form-label text-start ps-2"
            style="width: 100%"
            ><b>Password</b></label
          >
          <input
            type="password"
            class="form-control"
            id="exampleInputPassword1"
            v-model="password"
          />
          <div class="form-text" style="width: 100%">
            <a class="link">Forgot password</a>
          </div>
        </div>
        <button class="btn btn-primary mb-5" @click="login">Submit</button>
        <div class="form-text">
          Don't have an account? <a class="link" href="/signup">Sign Up</a>
        </div>
      </form>
    </div>
  </div>
</template>
<script lang="ts" setup>
import { ref } from "vue";
import axios, { AxiosError } from "axios";
import router from "@/router";

const email = ref("");
const password = ref("");
const error = ref("");

const login = async (event: Event) => {
  event.preventDefault();
  try {
    let data = await axios.post(
      "http://localhost:5000/login",
      {
        Email: email.value,
        Password: password.value,
      },
      { withCredentials: true }
    );
    router.push({ path: "/home" });
  } catch (err: AxiosError) {
    error.value = err.response.data.error;
  }
  console.log(email.value);
  console.log(password.value);
};
</script>
