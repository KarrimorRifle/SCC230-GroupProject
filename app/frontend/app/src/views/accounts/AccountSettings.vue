<template>
  <div class="page">
    <h1 class="text-light py-3 m-0" style="background-color: #01404d">
      Account details
    </h1>
    <hr class="text-light m-0" />
    <div class="d-flex align-items-center">
      <form action="" class="px-3 card-body bg" @submit.prevent="">
        <div class="mt-5">
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
                v-model="FirstName"
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
                v-model="Surname"
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
                v-model="Email"
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
                placeholder="New Password"
                v-model="Password"
              />
            </div>
            <div class="col-2 text-start">
              <label for="firstName" class="col-form-label"
                >Password must be at least 8 characters long
              </label>
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
                v-model="Password2"
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
                placeholder="Confirm password"
                v-model="password"
                required
              />
            </div>
          </div>
        </div>
        <button class="btn btn-success mt-2 me-2 mb-2">UPDPATE</button>
        <button type="button" class="btn btn-secondary me-2" @click="setData">
          RESET
        </button>
        <button class="btn btn-danger">DELETE</button>
      </form>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import { getAccount } from "@/functions";
import axios, { AxiosError } from "axios";

const Email = ref("");
const Password = ref("");
const Password2 = ref("");
const password = ref("");
const FirstName = ref("");
const Surname = ref("");
const error = ref("");

const emailError = ref("");
const pass1Error = ref("");
const pass2Error = ref("");

const accountData = ref();

const setData = () => {
  Email.value = accountData.value.Email;
  FirstName.value = accountData.value.FirstName;
  Surname.value = accountData.value.Surname;
};

const fillData = async () => {
  accountData.value = await getAccount();
  setData();
};
fillData();

const updateDetails = async () => {
  if (password.value == "") return;

  if (Password.value == Password2.value) {
    pass2Error.value = "Values don't match";
  } else {
    pass2Error.value = "";
  }

  if (Password.value.length >= 8 || Password.value == "") pass1Error.value = "";
  else pass1Error.value = ">= 8";

  if (!Email.value.includes(".") || !Email.value.includes("@")) {
    emailError.value = "Valid email please";
  } else {
    emailError.value = "";
  }

  if (
    pass2Error.value != "" ||
    pass1Error.value != "" ||
    emailError.value != ""
  )
    return;

  let data: Record<string, string> = {};
  if (FirstName.value != accountData.value.FirstName)
    data["FirstName"] = FirstName.value;

  if (Surname.value != accountData.value.Surname)
    data["Surname"] = Surname.value;

  if (Email.value != accountData.value.Email) data["Email"] = Email.value;
  if (Password.value != password.value) data["Password"] = Password.value;

  data["password"] = password.value;

  try {
    axios.patch("http://localhost:5000/accounts", {
      withCredentials: true,
      ...data,
    });
  } catch (err: AxiosError | any) {
    error.value = err;
  }
};
</script>

<style lang="scss">
.page {
  height: 100vh;
  margin: 0px 10rem !important;
  background-color: #1d2b39;
}

button {
  font-weight: 600 !important;
}
</style>
