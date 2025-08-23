<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <RouterLink class="navbar-brand" to="/">Catálogo</RouterLink>

      <!-- Botón hamburguesa para móviles -->
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <RouterLink class="nav-link" to="/">Inicio</RouterLink>
          </li>

          <!-- ✅ Dropdown Administrar -->
          <li class="nav-item dropdown">
            <a
              class="nav-link dropdown-toggle"
              href="#"
              id="adminDropdown"
              role="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              Administrar
            </a>
            <ul class="dropdown-menu" aria-labelledby="adminDropdown">
              <li><RouterLink class="dropdown-item" to="/productos">Productos</RouterLink></li>
              <li><RouterLink class="dropdown-item" to="/categorias">Categorías</RouterLink></li>
              <li><RouterLink class="dropdown-item" to="/presentaciones">Presentaciones</RouterLink></li>
            </ul>
          </li>
        </ul>

        <!-- Lado derecho: Hola usuario + cerrar sesión -->
        <ul class="navbar-nav ms-auto">
          <li v-if="username" class="nav-item me-2 d-flex align-items-center text-light">
            Hola, {{ username }}
          </li>
          <li class="nav-item">
            <button class="btn btn-outline-light btn-sm" :disabled="loading" @click="logout">
              Cerrar sesión
            </button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import http from "@/api/http";

export default {
  name: "AppNavbar",
  data() {
    return { loading: false };
  },
  computed: {
    username() {
      return sessionStorage.getItem("username") || "";
    },
  },
  methods: {
    async logout() {
      this.loading = true;
      try {
        await http.post("/auth/logout");
      } catch (e) {
        console.error(e);
      } finally {
        sessionStorage.removeItem("access_token");
        sessionStorage.removeItem("username");
        this.loading = false;
        this.$router.push("/login");
      }
    },
  },
};
</script>
