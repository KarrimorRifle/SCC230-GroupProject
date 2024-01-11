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
      <form action="" class="p-3 pb-0 card-body">
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
          />
          <div class="form-text" style="width: 100%">
            <a class="link">Forgot password</a>
          </div>
        </div>
        <button type="submit" class="btn btn-primary mb-5" @click="login()">
          Submit
        </button>
        <div class="form-text">
          Don't have an account? <a class="link" href="/signup">Sign Up</a>
        </div>
      </form>
    </div>
  </div>
</template>
<script lang="ts" setup>
const login = () => {
  console.log("logging in...");
};
</script>
