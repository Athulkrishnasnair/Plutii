<script setup lang="ts">
// Define props
defineProps({
    note: {
        type: Object,
        required: true,
    }
})

// Define emites
const emit = defineEmits(["edit", "delete"]);
</script>

<template>
    <article class="note-card">
        <h2>{{ note.title }}</h2>
        <p>{{ note.content }}</p>
    </article>

    <div class="actions">
        <button @click="$emit('edit', note)">Edit</button>
        <button @click="$emit('delete', note.id)">Delete</button>
   </div>
</template>

<style lang="css" scoped>
.note-card {
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 12px;
  background: white;
}

.note-card h2 {
  margin-top: 0;
}

.note-card p {
  white-space: pre-wrap;
}

.actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}
</style>