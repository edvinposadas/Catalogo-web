import { createRouter, createWebHistory } from "vue-router";
import LoginView from "@/views/LoginView.vue";
import RegisterView from "@/views/RegisterView.vue";
import PublicHome from "@/views/PublicHome.vue";
import DashboardView from "@/views/DashboardView.vue";
import CategoriaView from "@/views/CategoriaView.vue";
import PresentacionView from "@/views/PresentacionView.vue";
import ProductoView from "@/views/ProductoView.vue";

const routes = [
  { path: "/home", component: PublicHome, meta: { public: true } }, // Home pública (sin sesión)
  { path: "/login", component: LoginView, meta: { public: true } },
  { path: "/register", component: RegisterView, meta: { public: true } },

  { path: "/", name: "inicio", component: DashboardView },          // Inicio con el mensaje
  { path: "/categorias", component: CategoriaView },
  { path: "/presentaciones", component: PresentacionView },
  { path: "/productos", component: ProductoView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Guard único
router.beforeEach((to, from, next) => {
  const token = sessionStorage.getItem("access_token");
  const isPublic = !!(to.meta && to.meta.public);
  const free = ["/login", "/register"];
  if (isPublic || free.includes(to.path)) return next();
  if (!token) return next("/login");
  next();
});

export default router;
