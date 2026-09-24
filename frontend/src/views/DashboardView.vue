<template>
    <Navbar />

    <main class="dashboard">

        <header class="dashboard-header">
            <div>
                <h1>Your Notes</h1>
                <p>Keep your thoughts organised.</p>
            </div>

            <button
                class="new-note"
                @click="openCreateForm"
            >
                + New Note
            </button>
        </header>

        <section class="notes-grid">
            <NoteCard
                v-for="note in notes"
                :key="note.id"
                :note="note"
                @edit="openEditForm"
                @delete="handleDelete"
            />
        </section>

        <NoteForm
            v-if="showForm"
            :note="selectedNote"
            @save="saveNote"
            @cancel="closeForm"
        />

    </main>
</template>

<script setup>
// Import ref, onmounted and other comps
import { onMounted, ref } from 'vue';

import NoteCard from '../components/NoteCard.vue';
import NoteForm from '../components/NoteForm.vue';
import Navbar from '../components/Navbar.vue';

import { getNotes, createNote, updateNote, deleteNote } from '../services/api.js';

// Adding reactive vars
const notes = ref([]);
const selectedNote = ref(null);
const showForm = ref(false)

// Server code
async function loadNotes() {
    notes.value = await getNotes();
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

// Closes the form 
function closeForm() {
    selectedNote.value = null;
    showForm.value = false;
}

// Run when app runs
onMounted(loadNotes);

</script>

<style scoped>
.dashboard {
    max-width: 1200px;
    margin: 0 auto;
    padding: 32px 24px;
}

/* ───────── Header ───────── */

.dashboard-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    margin-bottom: 32px;
}

.dashboard-header h1 {
    margin: 0;
    color: #222;
    font-size: 2rem;
    font-weight: 700;
    letter-spacing: -0.5px;
}

.dashboard-header p {
    margin: 6px 0 0;
    color: #777;
    font-size: 0.95rem;
}

/* ───────── Primary button ───────── */

.new-note {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;

    padding: 10px 18px;

    border: none;
    border-radius: 10px;

    background: #42b883;
    color: white;

    font-size: 0.9rem;
    font-weight: 600;

    cursor: pointer;

    box-shadow: 0 4px 12px rgba(66, 184, 131, 0.22);

    transition:
        background 0.2s ease,
        transform 0.2s ease,
        box-shadow 0.2s ease;
}

.new-note:hover {
    background: #369f70;
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(66, 184, 131, 0.28);
}

.new-note:active {
    transform: translateY(0);
}

.new-note:focus-visible {
    outline: 3px solid rgba(66, 184, 131, 0.25);
    outline-offset: 2px;
}

/* ───────── Notes grid ───────── */

.notes-grid {
    display: grid;
    grid-template-columns: repeat(
        auto-fill,
        minmax(250px, 1fr)
    );
    gap: 20px;
}

/* ───────── Form buttons ───────── */

button {
    padding: 9px 16px;

    border: none;
    border-radius: 9px;

    font-size: 0.9rem;
    font-weight: 600;

    cursor: pointer;

    transition:
        background 0.2s ease,
        transform 0.2s ease;
}

button:hover {
    transform: translateY(-1px);
}

button:active {
    transform: translateY(0);
}

button[type="submit"] {
    background: #42b883;
    color: white;
}

button[type="submit"]:hover {
    background: #369f70;
}

button[type="button"] {
    background: #f1f1f2;
    color: #555;
}

button[type="button"]:hover {
    background: #e5e5e7;
}

button:focus-visible {
    outline: 3px solid rgba(66, 184, 131, 0.25);
    outline-offset: 2px;
}

/* ───────── Mobile ───────── */

@media (max-width: 600px) {
    .dashboard {
        padding: 24px 16px;
    }

    .dashboard-header {
        align-items: stretch;
        flex-direction: column;
    }

    .new-note {
        width: 100%;
    }

    .notes-grid {
        grid-template-columns: 1fr;
    }
}
</style>