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
      <h3 class="m-0">Sign Up</h3>
      <div class="text-warning" style="min-height: 1.5rem">{{ error }}</div>
      <hr class="m-0" />
      <form action="" class="px-3 card-body bg" @submit.prevent="signup()">
        <div class="mb-3">
          <input
            type="text"
            class="form-control mb-4"
            aria-describedby="emailHelp"
            placeholder="First name"
            v-model="first"
            required
          />
          <input
            type="text"
            class="form-control mb-4"
            aria-describedby="emailHelp"
            placeholder="Surname"
            v-model="sur"
            required
          />
          <input
            type="email"
            class="form-control"
            id="email"
            aria-describedby="emailHelp"
            placeholder="Email@example.com"
            v-model="email"
          />
          <div style="min-height: 1.3rem" class="form-text text-warning">
            {{ emailError }}
          </div>
          <input
            type="password"
            class="form-control"
            id="pass1"
            placeholder="Password"
            v-model="pass1"
          />
          <div style="min-height: 1.3rem" class="form-text text-warning">
            {{ pass1Error }}
          </div>
          <input
            type="password"
            class="form-control"
            id="pass2"
            placeholder="repeat Password"
            v-model="pass2"
          />
          <div style="min-height: 1.3rem" class="form-text text-warning">
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
import axios, { AxiosError } from "axios";
import router from "@/router";

const email = ref("");
const pass1 = ref("");
const pass2 = ref("");
const first = ref("");
const sur = ref("");
const error = ref("");

const emailError = ref("");
const pass1Error = ref("");
const pass2Error = ref("");

const signup = async () => {
  event.preventDefault();
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

  if (
    emailError.value != "" ||
    pass1Error.value != "" ||
    pass2Error.value != ""
  )
    return;

  //send api request
  email.value = email.value.toLocaleLowerCase();

  first.value =
    first.value.charAt(0).toUpperCase() +
    first.value.slice(1).toLocaleLowerCase();

  sur.value =
    sur.value.charAt(0).toUpperCase() + sur.value.slice(1).toLocaleLowerCase();

  try {
    await axios.post(
      "http://localhost:5000/accounts",
      {
        Email: email.value,
        Password: pass1.value,
        FirstName: first.value,
        Surname: sur.value,
      },
      { withCredentials: true }
    );
    router.push("/home");
  } catch (err: AxiosError) {
    error.value = err.response.data.error;
  }
};
</script>

<style>
a.link {
  text-decoration: underline !important;
  cursor: pointer;
}

.bg {
  background-color: #1d2b39;
}
</style>
