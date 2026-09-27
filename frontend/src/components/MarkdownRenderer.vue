<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { renderMarkdown, renderInlineMarkdown } from '../utils/markdown';
import { getHighlighterInstance } from '../services/highlighter';

const props = defineProps({
    content: {
        type: String,
        default: ''
    },
    inline: {
        type: Boolean,
        default: false
    }
});

const isHighlighterReady = ref(false);

onMounted(async () => {
    await getHighlighterInstance();
    isHighlighterReady.value = true;
});

const renderedHtml = computed(() => {
    // depend on isHighlighterReady to trigger re-compute once Shiki finishes loading
    const _ = isHighlighterReady.value;
    if (!props.content) return '';
    return props.inline ? renderInlineMarkdown(props.content) : renderMarkdown(props.content);
});
</script>

<template>
    <span
        v-if="inline"
        class="al-markdown al-markdown--inline"
        v-html="renderedHtml"
    ></span>
    <div
        v-else
        class="al-markdown"
        v-html="renderedHtml"
    ></div>
</template>

<style>
/* Global unscoped markdown styling scoped to .al-markdown container */
.al-markdown {
    color: var(--text-h);
    font-size: 0.875rem;
    line-height: 1.6;
    word-break: break-word;
}

.al-markdown--inline {
    display: inline;
}

.al-markdown p {
    margin: 0 0 var(--space-3) 0;
    color: var(--text-h);
}

.al-markdown p:last-child {
    margin-bottom: 0;
}

.al-markdown h1,
.al-markdown h2,
.al-markdown h3,
.al-markdown h4,
.al-markdown h5,
.al-markdown h6 {
    font-family: var(--heading);
    font-weight: 700;
    color: var(--text-h);
    margin: var(--space-4) 0 var(--space-2) 0;
    line-height: 1.3;
}

.al-markdown h1:first-child,
.al-markdown h2:first-child,
.al-markdown h3:first-child,
.al-markdown h4:first-child {
    margin-top: 0;
}

.al-markdown h1 { font-size: 1.25rem; }
.al-markdown h2 { font-size: 1.1rem; }
.al-markdown h3 { font-size: 0.95rem; }
.al-markdown h4 { font-size: 0.875rem; }

.al-markdown strong {
    font-weight: 700;
    color: var(--text-h);
}

.al-markdown em {
    font-style: italic;
}

.al-markdown ul,
.al-markdown ol {
    margin: 0 0 var(--space-3) 0;
    padding-left: var(--space-5);
}

.al-markdown ul:last-child,
.al-markdown ol:last-child {
    margin-bottom: 0;
}

.al-markdown li {
    margin-bottom: var(--space-1);
}

.al-markdown blockquote {
    margin: var(--space-3) 0;
    padding: var(--space-2) var(--space-4);
    border-left: 3px solid var(--accent);
    background: var(--surface-alt);
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    color: var(--text-muted);
}

.al-markdown blockquote p {
    margin: 0;
}

.al-markdown a {
    color: var(--accent);
    text-decoration: underline;
    text-underline-offset: 2px;
    transition: color var(--duration-fast);
}

.al-markdown a:hover {
    color: var(--text-h);
}

/* Inline code inside markdown */
.al-markdown :not(pre) > code {
    font-family: var(--mono);
    font-size: 0.8em;
    padding: 2px 5px;
    background: var(--surface-alt);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    color: var(--text-h);
    word-break: break-all;
}

/* Fenced code blocks inside markdown */
.al-markdown pre {
    margin: var(--space-3) 0;
    padding: var(--space-3) var(--space-4);
    border-radius: var(--radius-md);
    background: #181c24 !important;
    border: 1px solid var(--border);
    overflow-x: auto;
    font-family: var(--mono);
    font-size: 0.8rem;
    line-height: 1.5;
}

.al-markdown pre:last-child {
    margin-bottom: 0;
}

.al-markdown pre code {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    font-family: inherit;
    font-size: inherit;
    color: inherit;
}
</style>
