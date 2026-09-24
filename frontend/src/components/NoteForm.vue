<template>
    <form @submit.prevent="submitForm">
        <h2>{{ note ? "Edit note" : "Create note" }}</h2>

        <label for="title">Note title</label>
        <input type="text"
        placeholder="Note title"
        v-model="title"
        id="title"
        >

        <label for="content">Write a note</label>
        <textarea id="content"
        placeholder="Write your note"
        rows="6"
        v-model="content"
        ></textarea>

        <p v-if="error" class="error">{{ error }}</p>

        <div class="actions">
            <button type="submit">
                {{ note ? "Update" : "Create"}}
            </button>

            <button type="button" v-if="note"
            @click="$emit('cancel')"
            >Cancel</button>
        </div>
    </form>
</template>

<script setup>
import { ref, watch } from 'vue';

// Define a prop note
const props = defineProps({
    note: {
        type: Object,
        default: null
    }
   
})

// Define Emits
const emit = defineEmits(["save", "cancel"])

// Reactive variables
const title = ref('');
const content = ref('');
const error = ref('');

// When note changes
watch(
    () => props.note,
    (note) => {
        title.value = note?.title || "";
        content.value = note?.content || "";
    },
    {immediate: true}
);

// Form submit
function submitForm(){
    console.log('SUBMIT: ', title.value, content.value)

    error.value = '';

    if (!title.value.trim()) {
        error.value = 'Title is required';
        return;
    }

    if (!content.value.trim()) {
        error.value = 'Content is required';
        return;
    }


    emit('save', 
        {
            title: title.value,
            content: content.value
        }
    )
}

</script>

<style scoped>
form {
    display: flex;
    flex-direction: column;

    max-width: 700px;
    margin: 28px auto;
    padding: 28px;

    background: #ffffff;

    border: 1px solid #e5e7eb;
    border-radius: 16px;

    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.06);
}

h2 {
    margin: 0 0 18px;

    color: #222;
    font-size: 1.5rem;
    font-weight: 700;
}

/* Labels */

label {
    margin-bottom: 7px;

    color: #444;
    font-size: 0.9rem;
    font-weight: 600;
}

/* Inputs */

input,
textarea {
    width: 100%;
    box-sizing: border-box;

    padding: 12px 14px;

    border: 1px solid #d6d6d6;
    border-radius: 10px;

    background: #fafafa;
    color: #222;

    font: inherit;
    font-size: 0.95rem;

    outline: none;

    transition:
        border-color 0.2s ease,
        box-shadow 0.2s ease,
        background 0.2s ease;
}

input {
    margin-bottom: 10px;
}

textarea {
    min-height: 180px;
    resize: vertical;
}

input::placeholder,
textarea::placeholder {
    color: #999;
}

input:focus,
textarea:focus {
    background: #ffffff;
    border-color: #42b883;

    box-shadow: 0 0 0 3px rgba(66, 184, 131, 0.12);
}

/* Error */

.error {
    margin: 10px 0 0;

    color: #dc2626;
    font-size: 0.85rem;
}

/* Buttons */

.actions {
    display: flex;
    justify-content: flex-end;
    gap: 10px;

    margin-top: 20px;
}

.actions button {
    padding: 10px 17px;

    border: none;
    border-radius: 9px;

    font: inherit;
    font-size: 0.9rem;
    font-weight: 600;

    cursor: pointer;

    transition:
        background 0.2s ease,
        transform 0.2s ease,
        box-shadow 0.2s ease;
}

.actions button:hover {
    transform: translateY(-1px);
}

/* Create / Update */

.actions button[type="submit"] {
    background: #42b883;
    color: white;

    box-shadow: 0 4px 10px rgba(66, 184, 131, 0.2);
}

.actions button[type="submit"]:hover {
    background: #369f70;
    box-shadow: 0 6px 14px rgba(66, 184, 131, 0.25);
}

/* Cancel */

.actions button[type="button"] {
    background: #f1f1f2;
    color: #555;
}

.actions button[type="button"]:hover {
    background: #e5e5e7;
}

/* Keyboard accessibility */

.actions button:focus-visible {
    outline: 3px solid rgba(66, 184, 131, 0.25);
    outline-offset: 2px;
}

/* Mobile */

@media (max-width: 600px) {
    form {
        margin: 20px 0;
        padding: 20px;
    }

    .actions {
        flex-direction: column-reverse;
    }

    .actions button {
        width: 100%;
    }
}
</style>