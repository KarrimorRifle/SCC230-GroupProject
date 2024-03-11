import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import HomeView from "../views/HomeView.vue";
import LoginView from "../views/accounts/LoginView.vue";
import AccountSettings from "../views/accounts/AccountSettings.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
  },
  {
    path: "/signup",
    name: "sign up",
    component: () => import("../views/accounts/SignUp.vue"),
  },
  {
    path: "/account",
    name: "account settings",
    component: AccountSettings,
  },
  {
    path: "/about",
    name: "about",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
  },
  {
    path: "/schedules/:id",
    name: "schedules editor",
    component: () => import("../views/schedules/ScheduleEdit.vue"),
  },
  {
    path: "/schedules",
    name: "schedules",
    component: () => import("../views/schedules/ScheduleList.vue"),
  },
  {
    path: "/hubs",
    name: "hubs",
    component: () => import("../views/hubs/HubsList.vue"),
  },
  {
    path: "/hubs/:id",
    name: "hub viewer",
    component: () => import("../views/hubs/HubViewer.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
