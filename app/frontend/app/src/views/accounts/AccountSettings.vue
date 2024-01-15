<template>
  <div class="page">
    <h1 class="text-light py-3 m-0" style="background-color: #01404d">
      Account details
    </h1>
    <hr class="text-light m-0" />
    <div class="d-flex align-items-center">
      <form action="" class="px-3 card-body bg" @submit.prevent="lol()">
        <div class="mb-3 mt-5">
          <div class="row align-items-start g-3 text-light">
            <div class="col-2 text-start">
              <label for="firstName" class="col-form-label">First Name</label>
            </div>
            <div class="col-8">
              <input
                id="firstName"
                type="text"
                class="form-control mb-4"
                aria-describedby="emailHelp"
                placeholder="First name"
                v-model="first"
              />
            </div>
          </div>
          <div class="row align-items-start g-3 text-light">
            <div class="col-2 text-start">
              <label for="firstName" class="col-form-label">Surname</label>
            </div>
            <div class="col-8">
              <input
                type="text"
                class="form-control mb-4"
                aria-describedby="emailHelp"
                placeholder="Surname"
                v-model="sur"
              />
            </div>
          </div>
          <div class="row align-items-start g-3 text-light">
            <div class="col-2 text-start">
              <label for="firstName" class="col-form-label">Email</label>
            </div>
            <div class="col-8">
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
            </div>
          </div>
          <div class="row align-items-start g-3 text-light">
            <div class="col-2 text-start">
              <label for="firstName" class="col-form-label">New Password</label>
            </div>
            <div class="col-8">
              <input
                type="password"
                class="form-control"
                id="pass1"
                placeholder="new Password"
                v-model="pass1"
              />
              <div
                style="min-height: 1.3rem"
                class="form-text text-warning col-auto"
              >
                {{ pass1Error }}
              </div>
            </div>
          </div>
          <div class="row align-items-start g-3 text-light">
            <div class="col-2 text-start">
              <label for="firstName" class="col-form-label"
                >Repeat New Password</label
              >
            </div>
            <div class="col-8">
              <input
                type="password"
                class="form-control"
                id="pass2"
                placeholder="Repeat new password"
                v-model="pass2"
              />
              <div
                style="min-height: 1.3rem"
                class="form-text text-warning col-auto"
              >
                {{ pass2Error }}
              </div>
            </div>
          </div>
          <div class="row align-items-start g-3 text-light">
            <div class="col-2 text-start">
              <label for="firstName" class="col-form-label">Old Password</label>
            </div>
            <div class="col-8">
              <input
                type="password"
                class="form-control"
                id="pass2"
                placeholder="confirm password"
                v-model="pass2"
              />
            </div>
          </div>
        </div>
        <button class="btn btn-primary my-3">Change Details</button>
      </form>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import axios, { AxiosError } from "axios";

const email = ref("");
const pass1 = ref("");
const pass2 = ref("");
const first = ref("");
const sur = ref("");
const error = ref("");

const emailError = ref("");
const pass1Error = ref("");
const pass2Error = ref("");

const accountData = ref();

const lol = () => {
  return "arf";
};

// try {
//   accountData.value = await axios.get("http://localhost:5000/accounts");
// } catch (e: AxiosError) {
//   accountData.value = e;
// }
</script>

<style lang="scss">
.page {
  height: 100vh;
  margin: 0px 10rem !important;
  background-color: #1d2b39;
}
</style>
