<template>
  <ul class="dropdown-menu dropdown-menu-end me-3">
    <form action="" v-if="!loggedIn" class="p-3 pb-0">
      <div class="mb-3">
        <label for="exampleInputEmail1" class="form-label">Email address</label>
        <input
          type="email"
          class="form-control"
          id="exampleInputEmail1"
          aria-describedby="emailHelp"
        />
      </div>
      <div class="mb-3">
        <label for="exampleInputPassword1" class="form-label">Password</label>
        <input
          type="password"
          class="form-control"
          id="exampleInputPassword1"
        />
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
      <div class="form-text">Don't have an account? <a>Sign Up</a></div>
    </form>
    <div v-else></div>
  </ul>
</template>
