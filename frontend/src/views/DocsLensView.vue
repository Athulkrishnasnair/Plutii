<script setup>
import { ref } from 'vue';
import { analyzeDocs, fetchDocsUrl } from '../services/api';
import Navbar from '../components/Navbar.vue';

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

function copyResult() {
    if (!result.value) return;
    const text = [
        `SUMMARY:\n${result.value.summary}`,
        `\nKEY CONCEPTS:\n${(result.value.key_concepts || []).map(c => `- ${c}`).join('\n')}`,
        `\nEXAMPLE:\n${result.value.example}`,
        `\nCOMMON MISTAKE:\n${result.value.common_mistake}`
    ].join('\n');

    navigator.clipboard.writeText(text);
    copied.value = true;
    setTimeout(() => {
        copied.value = false;
    }, 2000);
}
</script>

<template>
    <div class="al-app-shell">
        <Navbar />

        <main class="al-app-main" id="main-content">
            <div class="al-container">

                <!-- Header -->
                <header class="al-page-header">
                    <span class="al-page-eyebrow">02 / DOCS LENS</span>
                    <h1 class="al-page-title">Technical Documentation Distiller</h1>
                    <p class="al-page-desc">
                        Fetch from a live URL or paste API reference content. ArrowLens extracts
                        an executive summary, essential concepts, a working code example, and the most common developer mistake.
                    </p>
                </header>

                <div class="al-workspace al-workspace--natural">

                    <!-- Left: Input Workspace Panel -->
                    <section class="al-workspace__panel" aria-labelledby="docs-input-heading">
                        <div class="al-workspace__panel-header">
                            <span id="docs-input-heading">DOCUMENTATION SOURCE</span>
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

                        <div class="al-workspace__panel-body">
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
                            <form @submit.prevent="handleAnalyze" novalidate>
                                <div class="al-form-group">
                                    <label for="dl-docs" class="al-label">
                                        <span>Documentation Content (Editable)</span>
                                        <span class="field-required">*</span>
                                    </label>
                                    <textarea
                                        id="dl-docs"
                                        v-model="content"
                                        class="al-textarea"
                                        placeholder="Paste library reference, API specification, or migration guide here…"
                                        rows="11"
                                        required
                                        aria-required="true"
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
                    <section class="al-workspace__panel" aria-labelledby="docs-result-heading">
                        <div class="al-workspace__panel-header">
                            <span id="docs-result-heading">DISTILLED SPECIFICATION</span>
                            <button
                                v-if="result"
                                type="button"
                                class="text-link-btn"
                                @click="copyResult"
                            >
                                {{ copied ? 'Copied ✓' : 'Copy Summary' }}
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
                        <div v-else class="al-result" role="region" aria-label="Documentation analysis result">
                            <div class="al-result__section">
                                <span class="al-result__label">Summary</span>
                                <p class="al-result__value">{{ result.summary }}</p>
                            </div>

                            <div class="al-result__section">
                                <span class="al-result__label">Key Concepts</span>
                                <ul class="al-result__list">
                                    <li v-for="(concept, idx) in result.key_concepts" :key="idx">
                                        {{ concept }}
                                    </li>
                                </ul>
                            </div>

                            <div class="al-result__section">
                                <span class="al-result__label">Working Example</span>
                                <pre class="example-code-block"><code>{{ result.example }}</code></pre>
                            </div>

                            <div class="al-result__section">
                                <span class="al-result__label">Common Mistake to Avoid</span>
                                <div class="al-callout al-callout--warning">
                                    <p class="al-result__value">{{ result.common_mistake }}</p>
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
