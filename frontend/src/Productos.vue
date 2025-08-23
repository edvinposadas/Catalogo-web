<template>
  <div>
    <ProductoTable
      :productos="productos"
      :page="page"
      :limit="limit"
      :search="search"
      @buscar="buscar"
      @editar="editarProducto"
      @eliminar="eliminarProducto"
      @pagina-anterior="pageAnterior"
      @pagina-siguiente="pageSiguiente"
    />

    <ProductoForm
      v-if="mostrarFormulario"
      :form="form"
      :editando="editando"
      :categorias="categorias"
      :presentaciones="presentaciones"
      @guardar="guardarProducto"
      @cancelar="cancelar"
    />
  </div>
</template>

<script>
import ProductoTable from '@/components/ProductoTable.vue';
import ProductoForm from '@/components/ProductoForm.vue';

export default {
  components: { ProductoTable, ProductoForm },
  data() {
    return {
      productos: [],
      categorias: [],
      presentaciones: [],
      page: 1,
      limit: 5,
      search: '',
      form: {
        id: null,
        nombre: '',
        precio: 0,
        categoria_id: null,
        presentacion_id: null,
        activo: true
      },
      editando: false,
      mostrarFormulario: false
    };
  },
  mounted() {
    this.cargarProductos();
    this.cargarCategorias();
    this.cargarPresentaciones();
  },
  methods: {
    async cargarProductos() {
      const res = await fetch(`/api/productos/?page=${this.page}&limit=${this.limit}&search=${this.search}`);
      const data = await res.json();
      this.productos = data.productos;
    },
    async cargarCategorias() {
      const res = await fetch('/api/categorias/');
      this.categorias = await res.json();
    },
    async cargarPresentaciones() {
      const res = await fetch('/api/presentaciones/');
      this.presentaciones = await res.json();
    },
    buscar(valor) {
      this.search = valor;
      this.page = 1;
      this.cargarProductos();
    },
    pageAnterior() {
      if (this.page > 1) { this.page--; this.cargarProductos(); }
    },
    pageSiguiente() {
      this.page++; 
      this.cargarProductos();
    },
    editarProducto(p) {
      this.editando = true;
      this.form = { ...p, categoria_id: p.categoria_id, presentacion_id: p.presentacion_id };
      this.mostrarFormulario = true;
    },
    cancelar() {
      this.editando = false;
      this.mostrarFormulario = false;
      this.form = { id: null, nombre: '', precio: 0, categoria_id: null, presentacion_id: null, activo: true };
    },
    async guardarProducto(data) {
      const url = this.editando ? `/api/productos/${data.id}` : '/api/productos/';
      const method = this.editando ? 'PUT' : 'POST';

      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      if (res.ok) {
        alert(this.editando ? 'Producto actualizado' : 'Producto creado');
        this.cancelar();
        this.cargarProductos();
      } else {
        const err = await res.json();
        alert(err.error || 'Error');
      }
    },
    async eliminarProducto(p) {
      if (!confirm(`¿Eliminar producto ${p.nombre}?`)) return;

      const res = await fetch(`/api/productos/${p.id}`, { method: 'DELETE' });
      if (res.ok) {
        alert('Producto eliminado');
        this.cargarProductos();
      } else {
        alert('Error al eliminar');
      }
    }
  }
};
</script>
