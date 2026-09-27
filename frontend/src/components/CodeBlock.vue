<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { highlightCode, normalizeLanguage, detectLanguageFromPath, escapeHtml } from '../services/highlighter';

const props = defineProps({
    code: {
        type: String,
        default: ''
    },
    lang: {
        type: String,
        default: ''
    },
    filename: {
        type: String,
        default: ''
    },
    showCopy: {
        type: Boolean,
        default: true
    },
    showLineNumbers: {
        type: Boolean,
        default: false
    }
});

const highlightedHtml = ref('');
const copied = ref(false);

const effectiveLang = computed(() => {
    if (props.lang) return normalizeLanguage(props.lang);
    if (props.filename) return detectLanguageFromPath(props.filename);
    return 'text';
});

async function updateHighlight() {
    if (!props.code) {
        highlightedHtml.value = '';
        return;
    }
    try {
        const html = await highlightCode(props.code, effectiveLang.value);
        highlightedHtml.value = html;
    } catch (err) {
        console.warn('Highlight failed, using plain fallback:', err);
        highlightedHtml.value = `<pre class="shiki-fallback"><code>${escapeHtml(props.code)}</code></pre>`;
    }
}

watch(
    () => [props.code, props.lang, props.filename],
    () => {
        updateHighlight();
    },
    { immediate: true }
);

onMounted(() => {
    updateHighlight();
});

async function copyCode() {
    if (!props.code) return;
    try {
        await navigator.clipboard.writeText(props.code);
        copied.value = true;
        setTimeout(() => {
            copied.value = false;
        }, 2000);
    } catch (err) {
        console.error('Clipboard copy error:', err);
    }
}
</script>

<template>
    <div class="al-code-block" role="region" :aria-label="filename ? `Code for ${filename}` : 'Code snippet'">
        <!-- Optional Header -->
        <div v-if="filename || effectiveLang !== 'text' || showCopy" class="al-code-block__header">
            <div class="al-code-block__info">
                <span v-if="filename" class="al-code-block__filename">
                    <svg width="12" height="12" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                        <path d="M3 2.5h7l3 3V13a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1z" stroke="currentColor" stroke-width="1.3"/>
                        <path d="M10 2.5V6h3.5" stroke="currentColor" stroke-width="1.2"/>
                    </svg>
                    <code>{{ filename }}</code>
                </span>
                <span v-if="effectiveLang && effectiveLang !== 'text'" class="al-code-block__lang">
                    {{ effectiveLang }}
                </span>
            </div>

            <button
                v-if="showCopy"
                type="button"
                class="al-code-block__copy"
                :class="{ 'al-code-block__copy--copied': copied }"
                @click="copyCode"
                :aria-label="copied ? 'Copied code to clipboard' : 'Copy code snippet'"
            >
                <svg v-if="!copied" width="12" height="12" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                    <rect x="5" y="5" width="8" height="8" rx="1.5" stroke="currentColor" stroke-width="1.3"/>
                    <path d="M3 11V3.5A1.5 1.5 0 0 1 4.5 2H11" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
                </svg>
                <svg v-else width="12" height="12" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                    <path d="M3.5 8.5L6.5 11.5L12.5 4.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span>{{ copied ? 'Copied' : 'Copy' }}</span>
            </button>
        </div>

        <!-- Code Content Area -->
        <div
            v-if="highlightedHtml"
            class="al-code-block__content"
            v-html="highlightedHtml"
        ></div>
        <pre
            v-else
            class="al-code-block__content al-code-block__fallback"
            tabindex="0"
        ><code>{{ code }}</code></pre>
    </div>
</template>

<style>
.al-code-block {
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    background: #181c24;
    overflow: hidden;
    margin: var(--space-3) 0;
    box-sizing: border-box;
}

.al-code-block__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 6px 12px;
    background: rgba(255, 255, 255, 0.03);
    border-bottom: 1px solid var(--border);
    gap: 8px;
}

.al-code-block__info {
    display: flex;
    align-items: center;
    gap: 8px;
    min-width: 0;
}

.al-code-block__filename {
    display: flex;
    align-items: center;
    gap: 5px;
    font-family: var(--mono);
    font-size: 0.75rem;
    color: var(--text-h);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.al-code-block__filename code {
    background: none;
    border: none;
    padding: 0;
    font-family: inherit;
    color: inherit;
}

.al-code-block__lang {
    font-family: var(--mono);
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted);
    background: var(--surface-alt);
    padding: 1px 6px;
    border-radius: var(--radius-sm);
    border: 1px solid var(--border);
}

.al-code-block__copy {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: transparent;
    border: 1px solid var(--border);
    color: var(--text-muted);
    font-family: var(--mono);
    font-size: 0.7rem;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition: all var(--duration-fast);
    flex-shrink: 0;
}

.al-code-block__copy:hover {
    color: var(--text-h);
    background: rgba(255, 255, 255, 0.05);
    border-color: var(--border-strong);
}

.al-code-block__copy--copied {
    color: #10b981;
    border-color: rgba(16, 185, 129, 0.4);
    background: rgba(16, 185, 129, 0.1);
}

.al-code-block__content {
    overflow-x: auto;
    font-family: var(--mono);
    font-size: 0.8rem;
    line-height: 1.5;
}

.al-code-block__content pre {
    margin: 0 !important;
    padding: 12px 16px !important;
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    overflow-x: auto;
    font-family: inherit;
    font-size: inherit;
    line-height: inherit;
}

.al-code-block__content code {
    font-family: inherit;
    font-size: inherit;
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}

.al-code-block__fallback {
    margin: 0;
    padding: 12px 16px;
    color: var(--text-h);
    white-space: pre;
}
</style>
