<template>
  <ul class="dropdown-menu dropdown-menu-end">
    <li class="px-3">
      <b
        >Hello,<br />
        {{ User["FirstName"] + " " + User["Surname"] }}!</b
      >
    </li>
    <hr class="m-0 mt-2" />
    <li>
      <a class="dropdown-item" href="/account" type="button"> Settings</a>
    </li>
    <li>
      <button class="dropdown-item" type="button" @click="logout">
        Logout
      </button>
    </li>
  </ul>
</template>

<script lang="ts" setup>
const logout = () => {
  //handle logging out
  return "hi";
};

let User = {
  FirstName: "Dave",
  Surname: "Jone",
};
</script>
<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'AccountDropdown'
})
</script>
