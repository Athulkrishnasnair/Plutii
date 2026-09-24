<script setup>
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
        <div class="note-content">
            <h2>{{ note.title }}</h2>
            <p>{{ note.content }}</p>
        </div>

        <div class="actions">
            <button
                class="edit-button"
                @click="$emit('edit', note)"
            >
                Edit
            </button>

            <button
                class="delete-button"
                @click="$emit('delete', note.id)"
            >
                Delete
            </button>
        </div>
    </article>
</template>

<style scoped>
.note-card {
    display: flex;
    flex-direction: column;

    min-height: 180px;
    padding: 20px;

    background: #ffffff;

    border: 1px solid #e5e7eb;
    border-radius: 14px;

    box-shadow: 0 5px 18px rgba(0, 0, 0, 0.05);

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease,
        border-color 0.2s ease;
}

.note-card:hover {
    transform: translateY(-3px);

    border-color: #d8e8e1;

    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
}

/* Content */

.note-content {
    flex: 1;
}

.note-card h2 {
    margin: 0 0 10px;

    color: #222;
    font-size: 1.15rem;
    font-weight: 700;

    overflow-wrap: anywhere;
}

.note-card p {
    margin: 0;

    color: #666;
    font-size: 0.92rem;
    line-height: 1.6;

    white-space: pre-wrap;
    overflow-wrap: anywhere;
}

/* Actions */

.actions {
    display: flex;
    justify-content: flex-end;
    gap: 8px;

    margin-top: 20px;
}

.actions button {
    padding: 7px 12px;

    border: none;
    border-radius: 8px;

    font-size: 0.82rem;
    font-weight: 600;

    cursor: pointer;

    transition:
        background 0.2s ease,
        color 0.2s ease,
        transform 0.2s ease;
}

.actions button:hover {
    transform: translateY(-1px);
}

/* Edit */

.edit-button {
    background: #eef8f3;
    color: #369f70;
}

.edit-button:hover {
    background: #dff2e9;
}

/* Delete */

.delete-button {
    background: #fef2f2;
    color: #dc2626;
}

.delete-button:hover {
    background: #fee2e2;
}

/* Keyboard focus */

.actions button:focus-visible {
    outline: 3px solid rgba(66, 184, 131, 0.2);
    outline-offset: 2px;
}

/* Mobile */

@media (max-width: 600px) {
    .note-card {
        min-height: 150px;
    }

    .actions {
        justify-content: stretch;
    }

    .actions button {
        flex: 1;
    }
}
</style>