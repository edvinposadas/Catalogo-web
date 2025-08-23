<template>
  <div>
    <h2>{{ editando ? 'Editar' : 'Crear' }} Producto</h2>
    <form @submit.prevent="guardar">
      <input v-model="localForm.nombre" placeholder="Nombre" required />
      <input v-model.number="localForm.precio" type="number" placeholder="Precio" required />

      <select v-model.number="localForm.categoria_id" required>
        <option value="">Seleccione categoría</option>
        <option v-for="c in categorias" :key="c.id" :value="c.id">{{ c.nombre }}</option>
      </select>

      <select v-model.number="localForm.presentacion_id" required>
        <option value="">Seleccione presentación</option>
        <option v-for="p in presentaciones" :key="p.id" :value="p.id">{{ p.nombre }}</option>
      </select>

      <label>
        Activo
        <input type="checkbox" v-model="localForm.activo" />
      </label>

      <button type="submit">{{ editando ? 'Actualizar' : 'Crear' }}</button>
      <button type="button" @click="$emit('cancelar')">Cancelar</button>
    </form>
  </div>
</template>

<script>
export default {
  props: {
    form: Object,
    editando: Boolean,
    categorias: Array,
    presentaciones: Array
  },
  data() {
    return {
      // Copia local de la prop para no mutarla
      localForm: { ...this.form }
    }
  },
  watch: {
    form: {
      handler(newVal) {
        this.localForm = { ...newVal }
      },
      deep: true
    }
  },
  methods: {
    guardar() {
      // Emitimos la copia local al padre
      this.$emit('guardar', { ...this.localForm })
    }
  }
}
</script>
