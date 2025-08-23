<template>
  <div>
    <AppNavbar />
    <div class="container mt-4">
      <router-view />
    </div>
  </div>
</template>

<script>
import AppNavbar from "@/components/Navbar.vue";

export default {
  name: "AppLayout",
  components: { AppNavbar }
};
</script>

<style scoped>
.container {
  padding: 20px;
}
</style>
