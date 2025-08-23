<template>
  <section class="container py-5 text-center">
    <!-- Mensaje principal -->
    <h1 class="display-5 fw-bold mb-4">Bienvenido al Catálogo Web</h1>
    <p class="lead text-muted mb-5">
      Usa el menú <strong>Administrar</strong> para gestionar categorías, productos y presentaciones.
    </p>

    <!-- Accesos rápidos -->
    <div class="d-flex gap-2 justify-content-center flex-wrap mb-5">
      <router-link class="btn btn-primary" to="/categorias">Ir a Categorías</router-link>
      <router-link class="btn btn-outline-primary" to="/productos">Ir a Productos</router-link>
      <router-link class="btn btn-outline-primary" to="/presentaciones">Ir a Presentaciones</router-link>
    </div>

    <!-- Resumen con tarjetas -->
    <div class="row g-4">
      <div class="col-md-4">
        <div class="card shadow-sm border-0 h-100">
          <div class="card-body">
            <h5 class="card-title">Categorías</h5>
            <p class="card-text display-6 fw-bold">{{ categorias.length }}</p>
            <router-link to="/categorias" class="btn btn-sm btn-outline-primary">Ver detalles</router-link>
          </div>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card shadow-sm border-0 h-100">
          <div class="card-body">
            <h5 class="card-title">Productos</h5>
            <p class="card-text display-6 fw-bold">{{ productos.length }}</p>
            <router-link to="/productos" class="btn btn-sm btn-outline-primary">Ver detalles</router-link>
          </div>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card shadow-sm border-0 h-100">
          <div class="card-body">
            <h5 class="card-title">Presentaciones</h5>
            <p class="card-text display-6 fw-bold">{{ presentaciones.length }}</p>
            <router-link to="/presentaciones" class="btn btn-sm btn-outline-primary">Ver detalles</router-link>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import http from "../api/http.js";

export default {
  name: "DashboardView",
  data() {
    return {
      productos: [],
      categorias: [],
      presentaciones: []
    };
  },
  async mounted() {
    try {
      const productosRes = await http.get("/productos");
      this.productos = Array.isArray(productosRes.data) ? productosRes.data : (productosRes.data.items || []);

      const categoriasRes = await http.get("/categorias");
      this.categorias = Array.isArray(categoriasRes.data) ? categoriasRes.data : (categoriasRes.data.items || []);

      const presentacionesRes = await http.get("/presentaciones");
      this.presentaciones = Array.isArray(presentacionesRes.data) ? presentacionesRes.data : (presentacionesRes.data.items || []);
    } catch (error) {
      console.error("Error cargando datos:", error);
    }
  }
};
</script>
