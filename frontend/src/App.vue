<template>
  <AppNavbar v-if="showNavbar" />
  <RouterView />
</template>

<script>
import { computed } from "vue";
import { useRoute } from "vue-router";
import AppNavbar from "@/components/AppNavbar.vue";

export default {
  components: { AppNavbar },
  setup() {
    const route = useRoute();
    const token = () => sessionStorage.getItem("access_token");
    const showNavbar = computed(() => {
      const hidden = ["/login", "/register"];
      if (hidden.includes(route.path)) return false;
      return !!token();
    });
    return { showNavbar };
  },
};
</script>