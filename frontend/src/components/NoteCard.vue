<script setup>
defineProps({
    note: {
        type: Object,
        required: true,
    }
});

defineEmits(['edit', 'delete']);
</script>

<template>
    <article class="note-card" :aria-labelledby="`note-title-${note.id}`">
        <div class="note-card__header">
            <span class="note-card__tag" aria-hidden="true">NOTE // #{{ note.id }}</span>
            <div class="note-card__actions">
                <button
                    type="button"
                    class="note-btn-icon"
                    aria-label="Edit note"
                    title="Edit note"
                    @click="$emit('edit', note)"
                >
                    <svg width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                        <path d="M11.5 2.5a2.121 2.121 0 0 1 3 3L5 15l-4 1 1-4 9.5-9.5z" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </button>
                <button
                    type="button"
                    class="note-btn-icon note-btn-icon--danger"
                    aria-label="Delete note"
                    title="Delete note"
                    @click="$emit('delete', note.id)"
                >
                    <svg width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                        <path d="M2 4h12M5.5 4V2.5a1 1 0 0 1 1-1h3a1 1 0 0 1 1 1V4M6 7v5M10 7v5M3.5 4l.8 10a1 1 0 0 0 1 .9h5.4a1 1 0 0 0 1-.9l.8-10" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </button>
            </div>
        </div>

        <div class="note-card__body">
            <h3 :id="`note-title-${note.id}`" class="note-card__title">
                {{ note.title }}
            </h3>
            <p class="note-card__text">
                {{ note.content }}
            </p>
        </div>

        <div class="note-card__footer">
            <router-link
                :to="{ path: '/plan-lens', query: { note: note.content } }"
                class="note-plan-cta"
            >
                <span>Turn into Plan</span>
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true">
                    <path d="M2.5 7h9M8 3.5 11.5 7 8 10.5" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </router-link>
        </div>
    </article>
</template>

<style scoped>
.note-card {
    display: flex;
    flex-direction: column;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: var(--space-5);
    box-shadow: var(--shadow-sm);
    transition: border-color var(--duration-fast), transform var(--duration-fast), box-shadow var(--duration-fast);
    position: relative;
    border-top: 3px solid var(--border-strong);
}

.note-card:hover {
    border-color: var(--border-strong);
    border-top-color: var(--accent);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

.note-card__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: var(--space-3);
}

.note-card__tag {
    font-family: var(--mono);
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: var(--text-muted);
}

.note-card__actions {
    display: flex;
    align-items: center;
    gap: 4px;
}

.note-btn-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    background: transparent;
    border: 1px solid transparent;
    border-radius: var(--radius-sm);
    color: var(--text-muted);
    cursor: pointer;
    transition: background 0.15s, color 0.15s;
}

.note-btn-icon:hover {
    background: var(--surface-alt);
    color: var(--text-h);
    border-color: var(--border);
}

.note-btn-icon--danger:hover {
    background: var(--error-bg);
    color: var(--error);
    border-color: rgba(220, 38, 38, 0.25);
}

.note-card__body {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: var(--space-2);
}

.note-card__title {
    font-family: var(--heading);
    font-size: 1.05rem;
    font-weight: 600;
    color: var(--text-h);
    margin: 0;
    overflow-wrap: anywhere;
}

.note-card__text {
    font-size: 0.875rem;
    line-height: 1.6;
    color: var(--text);
    margin: 0;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
    max-height: 140px;
    overflow-y: auto;
}

.note-card__footer {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    margin-top: var(--space-4);
    padding-top: var(--space-3);
    border-top: 1px dashed var(--border);
}

.note-plan-cta {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-family: var(--mono);
    font-size: 0.775rem;
    font-weight: 600;
    color: var(--accent);
    text-decoration: none;
    transition: gap 0.15s;
}

.note-plan-cta:hover {
    gap: 9px;
    text-decoration: underline;
}
</style>