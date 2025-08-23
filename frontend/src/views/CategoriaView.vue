<template>
  <div class="container mt-4">
    <h2>Categorías</h2>

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
        {{ editando ? 'Actualizar' : 'Agregar' }} Categoría
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

    <!-- Tabla de Categorías -->
    <table class="table table-bordered">
      <thead>
        <tr>
          <th style="width: 80px;">ID</th>
          <th>Nombre</th>
          <th>Descripción</th>
          <th style="width: 180px;">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="categoria in categorias" :key="categoria.id">
          <td>{{ categoria.id }}</td>
          <td>{{ categoria.nombre }}</td>
          <td>{{ categoria.descripcion }}</td>
          <td>
            <button class="btn btn-sm btn-warning me-2" @click="editarCategoria(categoria)">Editar</button>
            <button class="btn btn-sm btn-danger" @click="confirmarEliminar(categoria.id)">Eliminar</button>
          </td>
        </tr>
        <tr v-if="!loading && categorias.length === 0">
          <td colspan="4" class="text-center">Sin resultados</td>
        </tr>
        <tr v-if="loading">
          <td colspan="4" class="text-center">Cargando...</td>
        </tr>
      </tbody>
    </table>

    <!-- Paginación simple -->
    <nav>
      <ul class="pagination">
        <li class="page-item" :class="{ disabled: page === 1 || loading }">
          <button class="page-link" @click="cambiarPagina(page - 1)" :disabled="page === 1 || loading">Anterior</button>
        </li>
        <li class="page-item">
          <span class="page-link">{{ page }}</span>
        </li>
        <li class="page-item" :class="{ disabled: !haySiguiente || loading }">
          <button class="page-link" @click="cambiarPagina(page + 1)" :disabled="!haySiguiente || loading">Siguiente</button>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script>
import Swal from "sweetalert2";
import http from "@/api/http"; // axios con interceptores (access + refresh)

export default {
  name: "CategoriaView",
  data() {
    return {
      categorias: [],
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
      // si total viene del backend, calcula si hay más páginas;
      // si no hay total (array plano), habilita "Siguiente" siempre.
      if (typeof this.total === "number" && this.total >= 0) {
        return this.page * this.per_page < this.total;
      }
      return true;
    },
  },
  mounted() {
    this.cargarCategorias();
  },
  methods: {
    async cargarCategorias() {
      this.loading = true;
      try {
        // Backend acepta 'search' o 'q', y 'per_page' o 'size'
        const params = {
          page: this.page,
          per_page: this.per_page,
          search: this.search?.trim() || "",
        };
        const { data } = await http.get("/categorias/", { params });

        // ✅ Soporta array plano o paginado { items: [], total, page, per_page }
        const items = Array.isArray(data)
          ? data
          : (Array.isArray(data?.items) ? data.items : (Array.isArray(data?.data) ? data.data : []));

        this.categorias = items;
        this.total = Number.isFinite(data?.total) ? data.total : items.length;
        // si backend nos devolvió la página/por-página efectiva, sincroniza:
        if (Number.isFinite(data?.page)) this.page = data.page;
        if (Number.isFinite(data?.per_page)) this.per_page = data.per_page;
      } catch (e) {
        console.error(e);
        this.categorias = [];
        Swal.fire("Error", e?.response?.data?.error || "Error al cargar categorías", "error");
      } finally {
        this.loading = false;
      }
    },

    // debounce simple para la búsqueda
    onSearchInput() {
      clearTimeout(this.searchTimer);
      this.searchTimer = setTimeout(() => {
        this.page = 1;
        this.cargarCategorias();
      }, 350);
    },

    async confirmarGuardar() {
      const result = await Swal.fire({
        title: "¿Está seguro que desea guardar la información ingresada?",
        icon: "question",
        showCancelButton: true,
        confirmButtonText: "Sí, guardar",
        cancelButtonText: "Cancelar"
      });
      if (result.isConfirmed) this.guardarCategoria();
    },

    async guardarCategoria() {
      if (!this.form.nombre?.trim()) {
        Swal.fire("Validación", "El nombre es requerido", "warning");
        return;
      }

      this.loading = true;
      try {
        const url = this.editando ? `/categorias/${this.form.id}` : `/categorias/`;
        const method = this.editando ? "put" : "post";
        const payload = {
          nombre: this.form.nombre?.trim(),
          descripcion: this.form.descripcion?.trim() || null,
        };

        const { status, data } = await http[method](url, payload);

        if (!String(status).startsWith("2")) {
          throw new Error(data?.error || "Error al guardar la categoría");
        }

        this.resetForm();
        this.editando = false;
        await this.cargarCategorias();
        Swal.fire("Éxito", "Categoría guardada correctamente", "success");
      } catch (e) {
        console.error(e);
        Swal.fire("Error", e?.response?.data?.error || "Error al guardar la categoría", "error");
      } finally {
        this.loading = false;
      }
    },

    async editarCategoria(categoria) {
      const result = await Swal.fire({
        title: "¿Editar categoría?",
        text: `¿Deseas editar la categoría "${categoria.nombre}"?`,
        icon: "question",
        showCancelButton: true,
        confirmButtonText: "Sí, editar",
        cancelButtonText: "Cancelar"
      });

      if (result.isConfirmed) {
        this.form = { id: categoria.id, nombre: categoria.nombre, descripcion: categoria.descripcion || "" };
        this.editando = true;
        window.scrollTo({ top: 0, behavior: "smooth" });
      }
    },

    cancelarEdicion() {
      this.resetForm();
      this.editando = false;
    },

    async confirmarEliminar(id) {
      const result = await Swal.fire({
        title: "¿Estás seguro?",
        text: "No podrás revertir esta acción",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar"
      });

      if (result.isConfirmed) {
        this.eliminarCategoria(id);
      }
    },

    async eliminarCategoria(id) {
      this.loading = true;
      try {
        const { status, data } = await http.delete(`/categorias/${id}`);
        if (!String(status).startsWith("2")) {
          throw new Error(data?.error || "No se pudo eliminar");
        }
        Swal.fire("Eliminado", "La categoría ha sido eliminada", "success");
        // Si la página actual se queda sin elementos, retrocede una página
        if (this.categorias.length === 1 && this.page > 1) this.page -= 1;
        await this.cargarCategorias();
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

    cambiarPagina(nuevaPagina) {
      if (nuevaPagina < 1 || this.loading) return;
      this.page = nuevaPagina;
      this.cargarCategorias();
    }
  }
};
</script>
