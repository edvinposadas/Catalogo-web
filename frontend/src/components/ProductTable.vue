<template>
  <div>
    <input
      v-model="searchLocal"
      placeholder="Buscar por nombre"
      @input="$emit('buscar', searchLocal)"
    />

    <table border="1">
      <thead>
        <tr>
          <th>ID</th>
          <th>Nombre</th>
          <th>Precio</th>
          <th>Categoría</th>
          <th>Presentación</th>
          <th>Activo</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="p in productos" :key="p.id">
          <td>{{ p.id }}</td>
          <td>{{ p.nombre }}</td>
          <td>{{ p.precio }}</td>
          <td>{{ p.categoria }}</td>
          <td>{{ p.presentacion }}</td>
          <td>{{ p.activo ? 'Sí' : 'No' }}</td>
          <td>
            <button @click="$emit('editar', p)">Editar</button>
            <button @click="$emit('eliminar', p)">Eliminar</button>
          </td>
        </tr>
        <tr v-if="productos.length === 0">
          <td colspan="7" style="text-align:center">No hay productos</td>
        </tr>
      </tbody>
    </table>

    <div>
      <button @click="$emit('pagina-anterior')" :disabled="page===1">Anterior</button>
      <span>Página {{ page }}</span>
      <button @click="$emit('pagina-siguiente')" :disabled="productos.length < limit">Siguiente</button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    productos: Array,
    page: Number,
    limit: Number,
    search: String
  },
  data() {
    return {
      // Copia local de search para no mutar la prop
      searchLocal: this.search
    }
  },
  watch: {
    search(newVal) {
      this.searchLocal = newVal
    }
  }
}
</script>
