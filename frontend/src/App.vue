<script setup>
// Import ref, onmounted and other comps
import { onMounted, ref } from 'vue';

import NoteCard from './components/NoteCard.vue';
import NoteForm from './components/NoteForm.vue';

import { getNotes, createNote, updateNote, deleteNote } from './services/api.js';

// Adding reactive vars
const notes = ref([]);
const selectedNote = ref(null);
const showForm = ref(false)

// Server code
async function loadNotes() {
    notes.value = await getNotes();
    console.log(notes)
}

// Edit details
function openEditForm(note) {
    selectedNote.value = note;
    showForm.value = true;
}

// Create form-opener
// Clear selected notes and toggle visibility
function openCreateForm() {
  selectedNote.value = null;
  showForm.value = true
}

// Save the note
async function saveNote(noteData) {
  // if im editing updateNote
  // else createNote

  if (selectedNote.value) {
    await updateNote(selectedNote.value.id, noteData)
  }
  else {
    await createNote(noteData)
  }

  // Updating state
  await loadNotes();

  selectedNote.value = null;
  showForm.value = false;
}

// Delete a note
async function handleDelete(id) {
  await deleteNote(id);
  await loadNotes();
}

// Run when app runs
onMounted(loadNotes);
</script>

<template>
  <h1>Plutti</h1>
  <p>Your notes, organised.</p>

  <section>
    <NoteCard 
    v-for="note in notes"
    :key="note.id"
    @edit="openEditForm"
    :note="note"
    @delete="handleDelete"
    ></NoteCard>

  </section>

  <div class="createNote">
    <button
    @click="openCreateForm"
    >New Note</button>

    <NoteForm 
    v-if="showForm"
    :note="selectedNote"
    @save="saveNote"
    ></NoteForm>
  </div>
</template>

<style lang="css" scoped>
h1 {
  color: #42b883;
}
</style>