<template>
  <div class="container d-flex justify-content-center align-items-center" style="min-height: 70vh;">
    <div class="card shadow-sm" style="max-width: 480px; width: 100%;">
      <div class="card-body p-4">
        <h3 class="mb-3 text-center">Crear cuenta</h3>

        <form @submit.prevent="handleRegister" novalidate>
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
            <input
              v-model="password"
              :type="showPass ? 'text' : 'password'"
              class="form-control"
              autocomplete="new-password"
              required
              minlength="6"
            />
            <div class="form-text">Mínimo 6 caracteres.</div>
          </div>

          <div class="mb-3">
            <label class="form-label">Confirmar contraseña</label>
            <input
              v-model="password2"
              :type="showPass ? 'text' : 'password'"
              class="form-control"
              autocomplete="new-password"
              required
              minlength="6"
            />
          </div>

          <div class="form-check mb-3">
            <input class="form-check-input" type="checkbox" v-model="showPass" id="showPassChk" />
            <label class="form-check-label" for="showPassChk">Mostrar contraseñas</label>
          </div>

          <button :disabled="loading" type="submit" class="btn btn-success w-100">
            {{ loading ? 'Creando...' : 'Crear cuenta' }}
          </button>

          <p v-if="errorMessage" class="text-danger mt-3 mb-0">{{ errorMessage }}</p>
          <p v-if="successMessage" class="text-success mt-3 mb-0">{{ successMessage }}</p>

          <div class="text-center mt-3">
            <RouterLink to="/login">¿Ya tienes cuenta? Inicia sesión</RouterLink>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import http from "@/api/http";

export default {
  name: "RegisterView",
  data() {
    return {
      username: "",
      password: "",
      password2: "",
      showPass: false,
      loading: false,
      errorMessage: "",
      successMessage: "",
    };
  },
  methods: {
    async handleRegister() {
      this.errorMessage = "";
      this.successMessage = "";

      if (!this.username || !this.password || !this.password2) {
        this.errorMessage = "Completa todos los campos.";
        return;
      }
      if (this.password.length < 6) {
        this.errorMessage = "La contraseña debe tener al menos 6 caracteres.";
        return;
      }
      if (this.password !== this.password2) {
        this.errorMessage = "Las contraseñas no coinciden.";
        return;
      }

      this.loading = true;
      try {
        // Crear usuario
        const { data } = await http.post("/auth/register", {
          username: this.username,
          password: this.password,
        });

        this.successMessage = data?.message || "Cuenta creada con éxito.";

        // Opción A: redirigir al login
        setTimeout(() => this.$router.push("/login"), 700);

        // --- Opción B: autologin (descomenta si prefieres) ---
        // const login = await http.post("/auth/login", {
        //   username: this.username,
        //   password: this.password,
        // });
        // localStorage.setItem("access_token", login.data.access_token);
        // if (login.data?.user?.username) localStorage.setItem("username", login.data.user.username);
        // this.$router.push("/categorias");
      } catch (e) {
        this.errorMessage = e?.response?.data?.error || "No se pudo crear la cuenta.";
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>
