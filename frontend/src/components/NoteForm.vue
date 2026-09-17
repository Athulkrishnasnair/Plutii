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
  gap: 0.75rem;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 12px;
}

input,
textarea {
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  font: inherit;
}

.actions {
  display: flex;
  gap: 0.5rem;
}
</style>