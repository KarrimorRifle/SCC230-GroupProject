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
            <a class="nav-link active" aria-current="page" href="#">Home</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">Link</a>
          </li>
          <li class="nav-item">
            <a class="nav-link disabled" aria-disabled="true">Disabled</a>
          </li>
        </ul>
        <form class="d-flex" role="search">
          <div class="nav-item">
            <a class="nav-link text-light" href="/login"> Log in </a>
          </div>
        </form>
      </div>
    </div>
  </nav>
</template>
<script lang="ts" setup>
let loggedIn = false;
</script>
