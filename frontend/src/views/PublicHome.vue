<template>
  <section class="container py-5">
    <div class="text-center mb-4">
      <h1 class="fw-bold">Catálogo Web</h1>
      <p class="text-muted">Gestiona categorías, presentaciones y productos con autenticación JWT.</p>
    </div>
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card shadow-sm">
          <div class="card-body p-4">
            <h4 class="mb-3">¿Qué puedes hacer?</h4>
            <ul class="mb-4">
              <li>Administrar <strong>categorías</strong> y <strong>presentaciones</strong>.</li>
              <li>Crear, editar y eliminar <strong>productos</strong>.</li>
              <li>Autenticación segura con <strong>JWT</strong> y renovación automática del token.</li>
            </ul>
            <div class="d-flex flex-wrap gap-2">
              <router-link class="btn btn-primary" to="/login">Iniciar sesión</router-link>
              <router-link class="btn btn-outline-primary" to="/register">Crear cuenta</router-link>
            </div>
            <hr class="my-4">
            <p class="mb-0 small text-muted">Nota: Las secciones de administración requieren iniciar sesión.</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
<script>
export default { name: "PublicHome" };
</script>