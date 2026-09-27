<script setup>
import { ref } from 'vue';
import { analyzeDocs, fetchDocsUrl } from '../services/api';
import Navbar from '../components/Navbar.vue';
import MarkdownRenderer from '../components/MarkdownRenderer.vue';
import CodeBlock from '../components/CodeBlock.vue';

const content = ref('');
const result = ref(null);
const loading = ref(false);
const apiError = ref('');

// Web scraping state
const url = ref('');
const sourceUrl = ref('');
const fetching = ref(false);
const copied = ref(false);

function loadSample() {
    url.value = 'https://docs.python.org/3/library/collections.html#collections.defaultdict';
    sourceUrl.value = 'https://docs.python.org/3/library/collections.html#collections.defaultdict';
    content.value = `class collections.defaultdict(default_factory=None, /[, ...])

Return a new dictionary-like object. defaultdict is a subclass of the built-in dict class. It overrides one method and adds one writable instance variable. The remaining functionality is the same as for the dict class and is not documented here.

The first argument provides the initial value for the default_factory attribute; it defaults to None. All remaining arguments are treated the same as if they were passed to the dict constructor, including keyword arguments.

When each key is first encountered, a value is inserted automatically using default_factory with zero arguments. If default_factory is None, accessing a non-existent key raises a KeyError just like a normal dictionary.`;
}

function clearAll() {
    content.value = '';
    url.value = '';
    sourceUrl.value = '';
    result.value = null;
    apiError.value = '';
}

async function fetchUrl() {
    if (!url.value.trim()) {
        apiError.value = 'Please provide a valid documentation URL to fetch.';
        return;
    }

    fetching.value = true;
    apiError.value = '';

    try {
        const data = await fetchDocsUrl(url.value.trim());
        content.value = data.content;
        sourceUrl.value = data.url;
    } catch (error) {
        apiError.value = error.message || 'Failed to fetch documentation from the specified URL.';
    } finally {
        fetching.value = false;
    }
}

async function handleAnalyze() {
    if (!content.value.trim()) {
        apiError.value = 'Please provide documentation content or fetch from a URL first.';
        return;
    }

    loading.value = true;
    apiError.value = '';
    result.value = null;

    try {
        result.value = await analyzeDocs(content.value.trim());
    } catch (error) {
        apiError.value = error.message || 'Failed to analyze documentation. Please check your connection and try again.';
    } finally {
        loading.value = false;
    }
}

function getDocsAiMarkdown() {
    if (!result.value) return '';
    const parts = [
        '# ArrowLens Documentation Analysis',
        '',
        '## Summary',
        result.value.summary || '',
        '',
        '## Key Concepts',
        ...(result.value.key_concepts || []).map(c => `- ${c}`),
        '',
        '## Example',
        '```',
        result.value.example || '',
        '```',
        '',
        '## Common Mistake',
        result.value.common_mistake || ''
    ];

    if (sourceUrl.value) {
        parts.push('', '## Source Reference', sourceUrl.value);
    }

    return parts.join('\n');
}

async function copyForAi() {
    const text = getDocsAiMarkdown();
    if (!text) return;

    try {
        await navigator.clipboard.writeText(text);
        copied.value = true;
        setTimeout(() => {
            copied.value = false;
        }, 2000);
    } catch (e) {
        console.error('Clipboard copy failed:', e);
    }
}
</script>

<template>
    <div class="al-app-shell">
        <Navbar />

        <main class="al-app-main al-lens-page" id="main-content">
            <div class="al-container">

                <!-- Header -->
                <header class="al-page-header al-lens-header">
                    <div class="al-lens-eyebrow">
                        <span class="al-lens-eyebrow__icon al-lens-eyebrow__icon--docs" aria-hidden="true">
                            <svg width="13" height="13" viewBox="0 0 16 16" fill="none">
                                <path d="M3.5 2.5h6l3 3v8a1 1 0 0 1-1 1h-8a1 1 0 0 1-1-1v-10a1 1 0 0 1 1-1z" stroke="currentColor" stroke-width="1.3"/>
                                <path d="M9.5 2.5v3h3M5.5 8h5M5.5 10.5h3.5" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
                            </svg>
                        </span>
                        <span>DOCS LENS</span>
                    </div>
                    <h1 class="al-page-title">Technical Documentation Distiller</h1>
                    <p class="al-page-desc">
                        Fetch from a live URL or paste API reference content. ArrowLens extracts
                        an executive summary, essential concepts, a working code example, and the most common developer mistake.
                    </p>
                </header>

                <div class="al-lens-workspace">

                    <!-- Left: Input Workspace Panel -->
                    <section class="al-lens-panel" aria-labelledby="docs-input-heading">
                        <div class="al-lens-panel__header">
                            <div class="al-lens-panel__title">
                                <span id="docs-input-heading">DOCUMENTATION SOURCE</span>
                            </div>
                            <div class="panel-header-actions">
                                <button
                                    v-if="!content"
                                    type="button"
                                    class="text-link-btn"
                                    @click="loadSample"
                                >
                                    Load sample
                                </button>
                                <button
                                    v-else
                                    type="button"
                                    class="text-link-btn text-link-btn--danger"
                                    @click="clearAll"
                                >
                                    Clear
                                </button>
                            </div>
                        </div>

                        <div class="al-lens-panel__body">
                            <!-- Step 1: URL Fetcher Row -->
                            <div class="al-form-group">
                                <label for="docs-url" class="al-label">
                                    <span>Fetch from Documentation URL</span>
                                    <span class="label-step">STEP 1</span>
                                </label>
                                <div class="url-input-row">
                                    <input
                                        id="docs-url"
                                        v-model="url"
                                        type="url"
                                        class="al-input"
                                        placeholder="https://developer.mozilla.org/..."
                                        @keyup.enter="fetchUrl"
                                    />
                                    <button
                                        type="button"
                                        class="al-btn al-btn--secondary"
                                        :disabled="fetching || !url.trim()"
                                        @click="fetchUrl"
                                    >
                                        {{ fetching ? 'Fetching…' : 'Fetch' }}
                                    </button>
                                </div>
                            </div>

                            <!-- Source URL Metadata Pill (if fetched) -->
                            <div v-if="sourceUrl" class="docs-source-pill" role="status">
                                <span class="pill-label">SOURCE VERIFIED:</span>
                                <span class="pill-url">{{ sourceUrl }}</span>
                            </div>

                            <!-- Step 2: Documentation Editor Area -->
                            <form @submit.prevent="handleAnalyze" novalidate style="display: flex; flex-direction: column; flex: 1">
                                <div class="al-form-group" style="flex: 1; display: flex; flex-direction: column">
                                    <label for="dl-docs" class="al-label">
                                        <span>Documentation Content (Editable)</span>
                                        <span class="field-required">*</span>
                                    </label>
                                    <textarea
                                        id="dl-docs"
                                        v-model="content"
                                        class="al-textarea"
                                        placeholder="Paste library reference, API specification, or migration guide here…"
                                        rows="10"
                                        required
                                        aria-required="true"
                                        style="flex: 1; min-height: 180px"
                                    ></textarea>
                                </div>

                                <div v-if="apiError" class="al-status-error" role="alert" style="margin-top: 16px">
                                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true" style="flex-shrink: 0; margin-top: 2px">
                                        <circle cx="8" cy="8" r="7" stroke="currentColor" stroke-width="1.3"/>
                                        <path d="M8 5v3.5M8 11v.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                                    </svg>
                                    <span>{{ apiError }}</span>
                                </div>

                                <button
                                    type="submit"
                                    class="al-btn al-btn--primary"
                                    :disabled="loading || !content.trim()"
                                    style="margin-top: 20px; width: 100%; justify-content: center"
                                >
                                    <span v-if="loading" class="al-spinner" role="status" aria-label="Analyzing…"></span>
                                    <span v-else>Analyze Documentation</span>
                                    <svg v-if="!loading" aria-hidden="true" class="al-btn__arrow" width="16" height="16" viewBox="0 0 16 16" fill="none">
                                        <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                                    </svg>
                                </button>
                            </form>
                        </div>
                    </section>

                    <!-- Right: Distilled Result Panel -->
                    <section class="al-lens-panel" aria-labelledby="docs-result-heading">
                        <div class="al-lens-panel__header">
                            <div class="al-lens-panel__title">
                                <span id="docs-result-heading">DISTILLED SPECIFICATION</span>
                            </div>
                            <button
                                v-if="result"
                                type="button"
                                class="al-btn-copy-ai"
                                :class="{ 'al-btn-copy-ai--copied': copied }"
                                @click="copyForAi"
                                aria-label="Copy specification formatted for AI assistant"
                            >
                                <svg v-if="!copied" width="13" height="13" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                                    <rect x="5" y="5" width="8" height="8" rx="1.5" stroke="currentColor" stroke-width="1.3"/>
                                    <path d="M3 11V3.5A1.5 1.5 0 0 1 4.5 2H11" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
                                </svg>
                                <svg v-else width="13" height="13" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                                    <path d="M3.5 8.5L6.5 11.5L12.5 4.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                                </svg>
                                <span>{{ copied ? 'Copied' : 'Copy for AI' }}</span>
                            </button>
                        </div>

                        <!-- Loading State -->
                        <div v-if="loading" class="al-loading-state" role="status" aria-live="polite">
                            <div class="al-spinner"></div>
                            <span class="loading-title">DISTILLING DOCUMENTATION</span>
                            <span class="loading-sub">Extracting summary, concepts, code, and common pitfalls…</span>
                        </div>

                        <!-- Empty State -->
                        <div v-else-if="!result" class="al-empty-state">
                            <div class="al-empty-state__icon" aria-hidden="true">
                                <svg width="22" height="22" viewBox="0 0 20 20" fill="none">
                                    <rect x="3" y="2" width="14" height="16" rx="2" stroke="currentColor" stroke-width="1.3"/>
                                    <path d="M6 6h8M6 9h8M6 12h5" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
                                </svg>
                            </div>
                            <div class="al-empty-state__title">AWAITING DOCUMENTATION</div>
                            <p class="al-empty-state__desc">
                                Fetch a documentation URL or paste a reference text on the left to extract the key takeaways.
                            </p>
                        </div>

                        <!-- Structured Results Hierarchy -->
                        <div v-else class="al-lens-artifact al-result" role="region" aria-label="Documentation analysis result">
                            <div class="al-result__section">
                                <span class="al-result__label">Summary</span>
                                <MarkdownRenderer :content="result.summary" class="al-result__value" />
                            </div>

                            <div class="al-result__section">
                                <span class="al-result__label">Key Concepts</span>
                                <ul class="al-result__list">
                                    <li v-for="(concept, idx) in result.key_concepts" :key="idx">
                                        <MarkdownRenderer :content="concept" inline />
                                    </li>
                                </ul>
                            </div>

                            <div class="al-result__section">
                                <span class="al-result__label">Working Example</span>
                                <CodeBlock :code="result.example" lang="python" />
                            </div>

                            <div class="al-result__section">
                                <span class="al-result__label">Common Mistake to Avoid</span>
                                <div class="al-callout al-callout--warning">
                                    <MarkdownRenderer :content="result.common_mistake" class="al-result__value" />
                                </div>
                            </div>
                        </div>
                    </section>

                </div>

            </div>
        </main>
    </div>
</template>

<style scoped>
.panel-header-actions {
    display: flex;
    align-items: center;
    gap: 8px;
}

.text-link-btn {
    font-family: var(--mono);
    font-size: 0.7rem;
    font-weight: 600;
    color: var(--accent);
    background: none;
    border: none;
    cursor: pointer;
    padding: 0;
    text-decoration: underline;
}

.text-link-btn:hover {
    color: var(--text-h);
}

.text-link-btn--danger {
    color: var(--text-muted);
}
.text-link-btn--danger:hover {
    color: var(--error);
}

.label-step {
    font-size: 0.65rem;
    font-weight: 700;
    color: var(--accent);
}

.url-input-row {
    display: flex;
    gap: var(--space-2);
    min-width: 0;
}

.url-input-row .al-input {
    flex: 1;
    min-width: 0;
}

.docs-source-pill {
    display: flex;
    align-items: center;
    gap: 6px;
    min-width: 0;
    max-width: 100%;
    padding: 6px 12px;
    background: var(--accent-soft);
    border: 1px solid var(--accent-border);
    border-radius: var(--radius-sm);
    font-family: var(--mono);
    font-size: 0.725rem;
    color: var(--accent);
    overflow: hidden;
}

.pill-label {
    font-weight: 700;
    flex-shrink: 0;
}

.pill-url {
    min-width: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.example-code-block {
    background: var(--terminal-bg);
    color: var(--terminal-text);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: var(--space-4);
    font-family: var(--mono);
    font-size: 0.85rem;
    line-height: 1.6;
    overflow-x: auto;
    margin: 0;
    overflow-wrap: anywhere;
    word-break: break-word;
}

.loading-title {
    font-family: var(--mono);
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: var(--text-h);
}

.loading-sub {
    font-size: 0.85rem;
    color: var(--text-muted);
}
</style>
