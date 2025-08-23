<template>
  <div class="container d-flex justify-content-center align-items-center" style="min-height: 70vh;">
    <div class="card shadow-sm" style="max-width: 420px; width: 100%;">
      <div class="card-body p-4">
        <h3 class="mb-3 text-center">Iniciar sesión</h3>

        <form @submit.prevent="handleLogin" novalidate>
          <div class="mb-3">
            <label class="form-label">Usuario</label>
            <input
              v-model.trim="username"
              type="text"
              class="form-control"
              autocomplete="username"
              required
            />
          </div>

          <div class="mb-3">
            <label class="form-label">Contraseña</label>
            <div class="input-group">
              <input
                :type="showPass ? 'text' : 'password'"
                v-model="password"
                class="form-control"
                autocomplete="current-password"
                required
              />
              <button
                class="btn btn-outline-secondary"
                type="button"
                @click="showPass = !showPass"
                :disabled="loading"
                title="Mostrar/Ocultar"
              >
                {{ showPass ? 'Ocultar' : 'Mostrar' }}
              </button>
            </div>
          </div>

          <button :disabled="loading" type="submit" class="btn btn-primary w-100">
            {{ loading ? 'Ingresando...' : 'Entrar' }}
          </button>

          <p v-if="errorMessage" class="text-danger mt-3 mb-0">{{ errorMessage }}</p>
        </form>

        <!-- Enlaces debajo del formulario -->
        <div class="mt-3 text-center">
          <span>¿No tienes cuenta?</span>
          <router-link class="btn btn-link" to="/register">Crear cuenta</router-link>
        </div>
        <div class="mt-2 text-center">
          <router-link class="btn btn-secondary" to="/home">Ir a Home pública</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import http from "@/api/http";

export default {
  name: "LoginView",
  data() {
    return {
      username: "",
      password: "",
      errorMessage: "",
      loading: false,
      showPass: false,
    };
  },
  mounted() {
    // Si ya hay sesión activa, ir al Dashboard (Inicio)
    const token = sessionStorage.getItem("access_token");
    if (token) this.$router.replace("/");
  },
  methods: {
    async handleLogin() {
      this.errorMessage = "";
      if (!this.username || !this.password) {
        this.errorMessage = "Ingrese usuario y contraseña";
        return;
      }

      this.loading = true;
      try {
        // /auth/login devuelve access en JSON y setea refresh en cookie HTTPOnly
        const { data } = await http.post("/auth/login", {
          username: this.username,
          password: this.password,
        });

        // Guardar access token y (opcional) username para navbar
        sessionStorage.setItem("access_token", data.access_token);
        if (data?.user?.username) sessionStorage.setItem("username", data.user.username);

        // Ir al Dashboard (Inicio)
        this.$router.push("/");
      } catch (e) {
        this.errorMessage = e?.response?.data?.error || "Usuario o contraseña incorrectos";
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>
