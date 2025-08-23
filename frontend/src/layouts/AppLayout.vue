<template>
  <div>
    <!-- Navbar -->
    <Navbar />

    <!-- Contenido principal -->
    <div class="container mt-4">
      <router-view />
    </div>
  </div>
</template>

<script>

export default {
  name: "AppLayout",
  components: {
    Navbar,
  },
};
</script>

<style scoped>
/* Opcional: estilos generales del layout */
</style>
