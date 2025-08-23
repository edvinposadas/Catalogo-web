<template>
  <div class="container mt-4">
    <h2>Presentaciones</h2>

    <!-- Formulario Crear/Editar -->
    <form @submit.prevent="confirmarGuardar" class="mb-4">
      <div class="mb-3">
        <label class="form-label">Nombre</label>
        <input v-model.trim="form.nombre" type="text" class="form-control" required />
      </div>
      <div class="mb-3">
        <label class="form-label">Descripción</label>
        <input v-model.trim="form.descripcion" type="text" class="form-control" />
      </div>
      <button :disabled="loading" type="submit" class="btn btn-primary">
        {{ editando ? 'Actualizar' : 'Agregar' }} Presentación
      </button>
      <button v-if="editando" :disabled="loading" type="button" class="btn btn-secondary ms-2" @click="cancelarEdicion">
        Cancelar
      </button>
    </form>

    <!-- Filtro de búsqueda -->
    <div class="mb-3">
      <input
        v-model="search"
        type="text"
        class="form-control"
        placeholder="Buscar por nombre..."
        @input="onSearchInput"
      />
    </div>

    <!-- Tabla -->
    <table class="table table-bordered">
      <thead>
        <tr>
          <th style="width:80px;">ID</th>
          <th>Nombre</th>
          <th>Descripción</th>
          <th style="width:180px;">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="p in presentaciones" :key="p.id">
          <td>{{ p.id }}</td>
          <td>{{ p.nombre }}</td>
          <td>{{ p.descripcion }}</td>
          <td>
            <button class="btn btn-sm btn-warning me-2" @click="editar(p)">Editar</button>
            <button class="btn btn-sm btn-danger" @click="confirmarEliminar(p.id)">Eliminar</button>
          </td>
        </tr>
        <tr v-if="!loading && presentaciones.length === 0">
          <td colspan="4" class="text-center">Sin resultados</td>
        </tr>
        <tr v-if="loading">
          <td colspan="4" class="text-center">Cargando...</td>
        </tr>
      </tbody>
    </table>

    <!-- Paginación -->
    <nav>
      <ul class="pagination">
        <li class="page-item" :class="{ disabled: page === 1 || loading }">
          <button class="page-link" @click="cambiarPagina(page - 1)" :disabled="page === 1 || loading">Anterior</button>
        </li>
        <li class="page-item"><span class="page-link">{{ page }}</span></li>
        <li class="page-item" :class="{ disabled: !haySiguiente || loading }">
          <button class="page-link" @click="cambiarPagina(page + 1)" :disabled="!haySiguiente || loading">Siguiente</button>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script>
import Swal from "sweetalert2";
import http from "@/api/http";

export default {
  name: "PresentacionView",
  data() {
    return {
      presentaciones: [],
      form: { id: null, nombre: "", descripcion: "" },
      editando: false,
      page: 1,
      per_page: 10,
      total: 0,
      search: "",
      loading: false,
      searchTimer: null,
    };
  },
  computed: {
    haySiguiente() {
      if (typeof this.total === "number" && this.total >= 0) {
        return this.page * this.per_page < this.total;
      }
      return true;
    },
  },
  mounted() {
    this.cargar();
  },
  methods: {
    async cargar() {
      this.loading = true;
      try {
        const params = { page: this.page, per_page: this.per_page, search: this.search?.trim() || "" };
        const { data } = await http.get("/presentaciones/", { params });

        const items = Array.isArray(data)
          ? data
          : (Array.isArray(data?.items) ? data.items : (Array.isArray(data?.data) ? data.data : []));
        this.presentaciones = items;
        this.total = Number.isFinite(data?.total) ? data.total : items.length;
        if (Number.isFinite(data?.page)) this.page = data.page;
        if (Number.isFinite(data?.per_page)) this.per_page = data.per_page;
      } catch (e) {
        console.error(e);
        this.presentaciones = [];
        Swal.fire("Error", e?.response?.data?.error || "Error al cargar presentaciones", "error");
      } finally {
        this.loading = false;
      }
    },
    onSearchInput() {
      clearTimeout(this.searchTimer);
      this.searchTimer = setTimeout(() => {
        this.page = 1;
        this.cargar();
      }, 350);
    },
    async confirmarGuardar() {
      const result = await Swal.fire({
        title: "¿Guardar presentación?",
        icon: "question",
        showCancelButton: true,
        confirmButtonText: "Sí, guardar",
        cancelButtonText: "Cancelar",
      });
      if (result.isConfirmed) this.guardar();
    },
    async guardar() {
      if (!this.form.nombre?.trim()) {
        Swal.fire("Validación", "El nombre es requerido", "warning");
        return;
      }
      this.loading = true;
      try {
        const url = this.editando ? `/presentaciones/${this.form.id}` : `/presentaciones/`;
        const method = this.editando ? "put" : "post";
        const payload = { nombre: this.form.nombre?.trim(), descripcion: this.form.descripcion?.trim() || null };
        const { status, data } = await http[method](url, payload);
        if (!String(status).startsWith("2")) throw new Error(data?.error || "Error al guardar");
        this.resetForm();
        this.editando = false;
        await this.cargar();
        Swal.fire("Éxito", "Presentación guardada", "success");
      } catch (e) {
        console.error(e);
        Swal.fire("Error", e?.response?.data?.error || "No se pudo guardar", "error");
      } finally {
        this.loading = false;
      }
    },
    editar(p) {
      this.form = { id: p.id, nombre: p.nombre, descripcion: p.descripcion || "" };
      this.editando = true;
      window.scrollTo({ top: 0, behavior: "smooth" });
    },
    async confirmarEliminar(id) {
      const result = await Swal.fire({
        title: "¿Estás seguro?",
        text: "No podrás revertir esta acción",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar",
      });
      if (result.isConfirmed) this.eliminar(id);
    },
    async eliminar(id) {
      this.loading = true;
      try {
        const { status, data } = await http.delete(`/presentaciones/${id}`);
        if (!String(status).startsWith("2")) throw new Error(data?.error || "No se pudo eliminar");
        Swal.fire("Eliminado", "La presentación ha sido eliminada", "success");
        if (this.presentaciones.length === 1 && this.page > 1) this.page -= 1;
        await this.cargar();
      } catch (e) {
        console.error(e);
        Swal.fire("Error", e?.response?.data?.error || "Error de red al eliminar", "error");
      } finally {
        this.loading = false;
      }
    },
    resetForm() {
      this.form = { id: null, nombre: "", descripcion: "" };
    },
    cambiarPagina(n) {
      if (n < 1 || this.loading) return;
      this.page = n;
      this.cargar();
    },
  },
};
</script>
