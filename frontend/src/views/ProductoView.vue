<template>
  <div class="container mt-4">
    <h2>Productos</h2>

    <!-- Formulario Crear/Editar -->
    <form @submit.prevent="confirmarGuardar" class="mb-4">
      <div class="row g-3">
        <div class="col-md-4">
          <label class="form-label">Nombre</label>
          <input v-model.trim="form.nombre" type="text" class="form-control" required />
        </div>

        <div class="col-md-2">
          <label class="form-label">Precio</label>
          <input v-model.number="form.precio" type="number" min="0" step="0.01" class="form-control" required />
        </div>

        <div class="col-md-3">
          <label class="form-label">Categoría</label>
          <select v-model.number="form.categoria_id" class="form-select" required>
            <option disabled value="">Seleccione...</option>
            <option v-for="c in categorias" :key="c.id" :value="c.id">{{ c.nombre }}</option>
          </select>
        </div>

        <div class="col-md-3">
          <label class="form-label">Presentación</label>
          <select v-model.number="form.presentacion_id" class="form-select" required>
            <option disabled value="">Seleccione...</option>
            <option v-for="p in presentaciones" :key="p.id" :value="p.id">{{ p.nombre }}</option>
          </select>
        </div>

        <div class="col-md-12">
          <div class="form-check mt-2">
            <input class="form-check-input" type="checkbox" v-model="form.activo" id="chkActivo">
            <label class="form-check-label" for="chkActivo">Activo</label>
          </div>
        </div>
      </div>

      <div class="mt-3">
        <button :disabled="loading" type="submit" class="btn btn-primary">
          {{ editando ? 'Actualizar' : 'Agregar' }} Producto
        </button>
        <button v-if="editando" :disabled="loading" type="button" class="btn btn-secondary ms-2" @click="cancelarEdicion">
          Cancelar
        </button>
      </div>
    </form>

    <!-- Filtros -->
    <div class="row g-3 mb-3">
      <div class="col-md-6">
        <input
          v-model="search"
          type="text"
          class="form-control"
          placeholder="Buscar por nombre..."
          @input="onSearchInput"
        />
      </div>

      <div class="col-md-3">
        <select v-model.number="filtroCategoriaId" class="form-select" @change="onSearchInput">
          <option :value="null">Todas las categorías</option>
          <option v-for="c in categorias" :key="c.id" :value="c.id">{{ c.nombre }}</option>
        </select>
      </div>

      <div class="col-md-3">
        <select v-model.number="filtroPresentacionId" class="form-select" @change="onSearchInput">
          <option :value="null">Todas las presentaciones</option>
          <option v-for="p in presentaciones" :key="p.id" :value="p.id">{{ p.nombre }}</option>
        </select>
      </div>
    </div>

    <!-- Tabla -->
    <table class="table table-bordered">
      <thead>
        <tr>
          <th style="width:80px;">ID</th>
          <th>Nombre</th>
          <th style="width:120px;">Precio</th>
          <th style="width:160px;">Categoría</th>
          <th style="width:180px;">Presentación</th>
          <th style="width:100px;">Activo</th>
          <th style="width:180px;">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="p in productos" :key="p.id">
          <td>{{ p.id }}</td>
          <td>{{ p.nombre }}</td>
          <td>{{ Number(p.precio).toFixed(2) }}</td>
          <td>{{ categoriaNombre(p.categoria_id) }}</td>
          <td>{{ presentacionNombre(p.presentacion_id) }}</td>
          <td>
            <span class="badge" :class="p.activo ? 'bg-success' : 'bg-secondary'">
              {{ p.activo ? 'Sí' : 'No' }}
            </span>
          </td>
          <td>
            <button class="btn btn-sm btn-warning me-2" @click="editar(p)">Editar</button>
            <button class="btn btn-sm btn-danger" @click="confirmarEliminar(p.id)">Eliminar</button>
          </td>
        </tr>
        <tr v-if="!loading && productos.length === 0">
          <td colspan="7" class="text-center">Sin resultados</td>
        </tr>
        <tr v-if="loading">
          <td colspan="7" class="text-center">Cargando...</td>
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
  name: "ProductoView",
  data() {
    return {
      productos: [],
      categorias: [],
      presentaciones: [],
      form: { id: null, nombre: "", precio: 0, categoria_id: "", presentacion_id: "", activo: true },
      editando: false,
      page: 1,
      per_page: 10,
      total: 0,
      search: "",
      filtroCategoriaId: null,
      filtroPresentacionId: null,
      loading: false,
      searchTimer: null,
    };
  },
  computed: {
    haySiguiente() {
      return this.page * this.per_page < this.total;
    },
    categoriaMap() {
      const m = {};
      for (const c of this.categorias) m[c.id] = c.nombre;
      return m;
    },
    presentacionMap() {
      const m = {};
      for (const p of this.presentaciones) m[p.id] = p.nombre;
      return m;
    },
  },
  mounted() {
    this.cargarReferenciales().then(() => this.cargar());
  },
  methods: {
    categoriaNombre(id) { return this.categoriaMap[id] || "—"; },
    presentacionNombre(id) { return this.presentacionMap[id] || "—"; },

    async cargarReferenciales() {
      try {
        const [catRes, presRes] = await Promise.all([
          http.get("/categorias", { params: { page: 1, per_page: 1000 } }),
          http.get("/presentaciones", { params: { page: 1, per_page: 1000 } }),
        ]);
        this.categorias = Array.isArray(catRes.data) ? catRes.data : (catRes.data.items || []);
        this.presentaciones = Array.isArray(presRes.data) ? presRes.data : (presRes.data.items || []);
      } catch (e) {
        console.error(e);
        Swal.fire("Error", "No se pudieron cargar categorías/presentaciones", "error");
      }
    },

    async cargar() {
      this.loading = true;
      try {
        const params = {
          page: this.page,
          per_page: this.per_page,
          search: this.search?.trim() || "",
        };
        if (this.filtroCategoriaId) params.categoria_id = this.filtroCategoriaId;
        if (this.filtroPresentacionId) params.presentacion_id = this.filtroPresentacionId;

        const { data } = await http.get("/productos/", { params });
        const items = Array.isArray(data)
          ? data
          : (Array.isArray(data?.items) ? data.items : (Array.isArray(data?.data) ? data.data : []));
        this.productos = items;
        this.total = Number.isFinite(data?.total) ? data.total : items.length;
      } catch (e) {
        console.error(e);
        Swal.fire("Error", e?.response?.data?.error || "Error al cargar productos", "error");
      } finally {
        this.loading = false;
      }
    },

    onSearchInput() {
      clearTimeout(this.searchTimer);
      this.searchTimer = setTimeout(() => {
        this.page = 1;
        this.cargar();
      }, 300);
    },

    async confirmarGuardar() {
      const result = await Swal.fire({
        title: "¿Guardar producto?",
        icon: "question",
        showCancelButton: true,
        confirmButtonText: "Sí, guardar",
        cancelButtonText: "Cancelar",
      });
      if (result.isConfirmed) this.guardar();
    },

    async guardar() {
      const { nombre, precio, categoria_id, presentacion_id } = this.form;
      if (!nombre?.trim() || precio == null || categoria_id === "" || presentacion_id === "") {
        Swal.fire("Validación", "Completa los campos requeridos", "warning");
        return;
      }
      this.loading = true;
      try {
        const url = this.editando ? `/productos/${this.form.id}` : `/productos/`;
        const method = this.editando ? "put" : "post";
        const payload = {
          nombre: nombre.trim(),
          precio: Number(precio),
          categoria_id: Number(categoria_id),
          presentacion_id: Number(presentacion_id),
          activo: !!this.form.activo,
        };
        await http[method](url, payload);
        this.resetForm();
        this.editando = false;
        await this.cargar();
        Swal.fire("Éxito", "Producto guardado", "success");
      } catch (e) {
        console.error(e);
        Swal.fire("Error", e?.response?.data?.error || "No se pudo guardar", "error");
      } finally {
        this.loading = false;
      }
    },

    editar(p) {
      this.form = {
        id: p.id,
        nombre: p.nombre,
        precio: Number(p.precio),
        categoria_id: p.categoria_id,
        presentacion_id: p.presentacion_id,
        activo: !!p.activo,
      };
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
        await http.delete(`/productos/${id}`);
        Swal.fire("Eliminado", "El producto ha sido eliminado", "success");
        if (this.productos.length === 1 && this.page > 1) this.page -= 1;
        await this.cargar();
      } catch (e) {
        console.error(e);
        Swal.fire("Error", e?.response?.data?.error || "Error al eliminar", "error");
      } finally {
        this.loading = false;
      }
    },

    resetForm() {
      this.form = { id: null, nombre: "", precio: 0, categoria_id: "", presentacion_id: "", activo: true };
    },

    cambiarPagina(n) {
      if (n < 1 || this.loading) return;
      this.page = n;
      this.cargar();
    },
  },
};
</script>
