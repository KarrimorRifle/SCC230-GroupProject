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
import router from "@/router";
import axios from "axios";
import { deleteCookie } from "@/modules/common/functions";

const logout = async () => {
  let data;
  try {
    data = await axios.delete("http://localhost:5000/logout", {
      withCredentials: true,
    });
    deleteCookie("SessionID");
    router.push("home");
  } catch (e) {
    console.log(e);
    console.log(data);
  }
};

let User = {
  FirstName: "David",
  Surname: "Mellon",
};
</script>
<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "AccountDropdown",
});
</script>
