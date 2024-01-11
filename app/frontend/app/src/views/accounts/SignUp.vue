<template>
  <div
    class="d-flex align-items-start justify-content-center"
    style="height: 90vh"
    data-bs-theme="dark"
  >
    <div
      class="card"
      style="width: 35%; margin-top: 6rem; min-height: 23rem; padding-top: 1rem"
    >
      <form action="" class="p-3 pb-0 card-body" @submit.prevent="signup()">
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
            aria-describedby="emailHelp"
            v-model="email"
          />
          <div style="min-height: 1.5rem" class="form-text text-warning">
            {{ emailError }}
          </div>
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
            v-model="pass1"
          />
          <div style="min-height: 1.5rem" class="form-text text-warning">
            {{ pass1Error }}
          </div>
        </div>
        <div class="mb-3">
          <label
            for="exampleInputPassword1"
            class="form-label text-start ps-2"
            style="width: 100%"
            ><b>Repeat password</b></label
          >
          <input
            type="password"
            class="form-control"
            id="exampleInputPassword1"
            v-model="pass2"
          />
          <div style="min-height: 1.5rem" class="form-text text-warning">
            {{ pass2Error }}
          </div>
        </div>
        <button class="btn btn-primary my-3">Sign up</button>
      </form>
    </div>
  </div>
</template>
<script lang="ts" setup>
import { ref } from "vue";
const email = ref("");
const pass1 = ref("");
const pass2 = ref("");
const emailError = ref("");
const pass1Error = ref("");
const pass2Error = ref("");

const signup = () => {
  console.log(`email = ${email.value}`);
  console.log(`pass1 = ${pass1.value}`);
  console.log(`pass2 = ${pass2.value}`);
  //checking validity of email
  if (!email.value.includes("@") || !email.value.includes(".")) {
    emailError.value = "Input a valid email";
  } else {
    emailError.value = "";
  }
  //checking for a valid password
  if (pass1.value.length < 8) pass1Error.value = "Minimum length of 8";
  else pass1Error.value = "";
  //checking if passwords match
  if (pass1.value != pass2.value) pass2Error.value = "Passwords don't match";
  else pass2Error.value = "";

  //send api request
};
</script>

<style>
a.link {
  text-decoration: underline !important;
  cursor: pointer;
}
</style>
