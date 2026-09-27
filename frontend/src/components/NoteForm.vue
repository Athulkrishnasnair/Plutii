<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue';

const props = defineProps({
    note: {
        type: Object,
        default: null
    }
});

const emit = defineEmits(['save', 'cancel']);

const title = ref('');
const content = ref('');
const error = ref('');

watch(
    () => props.note,
    (n) => {
        title.value = n?.title || '';
        content.value = n?.content || '';
    },
    { immediate: true }
);

function submitForm() {
    error.value = '';

    if (!title.value.trim()) {
        error.value = 'A title is required for this note.';
        return;
    }

    if (!content.value.trim()) {
        error.value = 'Please provide content or an implementation idea.';
        return;
    }

    emit('save', {
        title: title.value.trim(),
        content: content.value.trim()
    });
}

function handleEscape(e) {
    if (e.key === 'Escape') {
        emit('cancel');
    }
}

onMounted(() => {
    window.addEventListener('keydown', handleEscape);
});

onUnmounted(() => {
    window.removeEventListener('keydown', handleEscape);
});
</script>

<template>
    <div
        class="note-modal-backdrop"
        @click.self="$emit('cancel')"
        role="dialog"
        aria-modal="true"
        :aria-label="note ? 'Edit Note' : 'Create New Note'"
    >
        <div class="note-modal-card">
            <header class="note-modal__header">
                <div>
                    <span class="note-modal__eyebrow">
                        DEVELOPER SCRATCHPAD
                    </span>
                    <h2 class="note-modal__title">
                        {{ note ? 'Edit Note' : 'Capture New Note' }}
                    </h2>
                </div>
                <button
                    type="button"
                    class="note-modal__close"
                    aria-label="Close form"
                    @click="$emit('cancel')"
                >
                    ×
                </button>
            </header>

            <form class="note-modal__form" @submit.prevent="submitForm" novalidate>
                <div class="al-form-group">
                    <label for="note-title-input" class="al-label">
                        Note Title <span class="field-required">*</span>
                    </label>
                    <input
                        id="note-title-input"
                        v-model="title"
                        type="text"
                        class="al-input"
                        :class="{ 'al-input--error': error && !title.trim() }"
                        placeholder="e.g. Asynchronous event retry architecture"
                        required
                        autofocus
                    />
                </div>

                <div class="al-form-group">
                    <label for="note-content-input" class="al-label">
                        Content / Implementation Spec <span class="field-required">*</span>
                    </label>
                    <textarea
                        id="note-content-input"
                        v-model="content"
                        class="al-textarea"
                        :class="{ 'al-textarea--error': error && !content.trim() }"
                        rows="7"
                        placeholder="Describe the technical idea, API contract, or error fix you want to turn into an implementation plan…"
                        required
                    ></textarea>
                </div>

                <div v-if="error" class="al-status-error" role="alert">
                    {{ error }}
                </div>

                <footer class="note-modal__actions">
                    <button
                        type="button"
                        class="al-btn al-btn--ghost"
                        @click="$emit('cancel')"
                    >
                        Cancel
                    </button>
                    <button
                        type="submit"
                        class="al-btn al-btn--primary"
                    >
                        {{ note ? 'Save Changes' : 'Save Note' }}
                    </button>
                </footer>
            </form>
        </div>
    </div>
</template>

<style scoped>
.note-modal-backdrop {
    position: fixed;
    inset: 0;
    z-index: 1000;
    background: rgba(10, 12, 16, 0.5);
    backdrop-filter: blur(4px);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: var(--space-4);
}

.note-modal-card {
    width: 100%;
    max-width: 560px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-lg);
    overflow: hidden;
    animation: modal-pop 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes modal-pop {
    from {
        opacity: 0;
        transform: scale(0.96) translateY(8px);
    }
    to {
        opacity: 1;
        transform: scale(1) translateY(0);
    }
}

.note-modal__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--space-6) var(--space-6) var(--space-4);
    border-bottom: 1px solid var(--border);
    background: var(--surface-alt);
}

.note-modal__eyebrow {
    font-family: var(--mono);
    font-size: 0.675rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: var(--text-muted);
    display: block;
    margin-bottom: 2px;
}

.note-modal__title {
    font-family: var(--heading);
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-h);
    margin: 0;
}

.note-modal__close {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: transparent;
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    color: var(--text-muted);
    font-size: 1.25rem;
    cursor: pointer;
    line-height: 1;
}

.note-modal__close:hover {
    background: var(--surface-active);
    color: var(--text-h);
}

.note-modal__form {
    padding: var(--space-6);
    display: flex;
    flex-direction: column;
    gap: var(--space-5);
}

.note-modal__actions {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: var(--space-3);
    padding-top: var(--space-4);
    border-top: 1px solid var(--border);
}
</style>