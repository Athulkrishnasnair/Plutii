<script setup>
import { ref, computed } from 'vue';
import ImplementationMap from '../components/ImplementationMap.vue';
import Navbar from '../components/Navbar.vue';
import { uploadCodebase, analyzeCodebase } from '../services/api';

const file = ref(null);
const files = ref([]);
const loading = ref(false);
const error = ref('');

// Query state
const query = ref('');
const analysis = ref(null);
const analyzing = ref(false);
const relationships = ref([]);
const fileFilter = ref('');

const filteredFiles = computed(() => {
    if (!fileFilter.value.trim()) return files.value;
    const q = fileFilter.value.toLowerCase();
    return files.value.filter(f => f.path.toLowerCase().includes(q));
});

function handleFileChange(event) {
    file.value = event.target.files[0] || null;
    error.value = '';
}

async function handleUpload() {
    if (!file.value) {
        error.value = 'Please select a repository ZIP archive to scan.';
        return;
    }

    loading.value = true;
    error.value = '';

    try {
        const data = await uploadCodebase(file.value);
        files.value = data.files || [];
        relationships.value = data.relationships || [];
    } catch (err) {
        error.value = err.message || 'Failed to scan and unpack codebase archive.';
    } finally {
        loading.value = false;
    }
}

async function handleAnalyze() {
    if (!query.value.trim()) {
        error.value = 'Please enter a question about your project codebase.';
        return;
    }

    analyzing.value = true;
    error.value = '';

    try {
        analysis.value = await analyzeCodebase(query.value.trim());
    } catch (err) {
        error.value = err.message || 'Codebase analysis failed. Please try again.';
    } finally {
        analyzing.value = false;
    }
}

function loadSuggestedQuery(q) {
    query.value = q;
}
</script>

<template>
    <div class="al-app-shell">
        <Navbar />

        <main class="al-app-main" id="main-content">
            <div class="al-container">

                <!-- Header -->
                <header class="al-page-header">
                    <span class="al-page-eyebrow">04 / CODEBASE LENS</span>
                    <h1 class="al-page-title">Codebase Topology & Structural Query</h1>
                    <p class="al-page-desc">
                        Upload a repository archive. ArrowLens parses module ASTs, maps dependency
                        relationships, and allows you to query where architecture boundaries and business logic reside.
                    </p>
                </header>

                <!-- Step 1: Upload Archive Section -->
                <section class="cb-section" aria-labelledby="upload-heading">
                    <div class="al-workspace__panel">
                        <div class="al-workspace__panel-header">
                            <span id="upload-heading">STEP 01 // UPLOAD REPOSITORY ARCHIVE</span>
                            <span v-if="files.length" class="cb-loaded-badge">
                                {{ files.length }} Files Indexed
                            </span>
                        </div>

                        <div class="al-workspace__panel-body">
                            <div class="cb-upload-zone">
                                <label for="codebase" class="cb-file-label">
                                    <div class="cb-upload-icon" aria-hidden="true">
                                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                                            <path d="M12 4v12M8 8l4-4 4 4M4 17v2a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-2" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
                                        </svg>
                                    </div>
                                    <span class="cb-upload-main">
                                        {{ file ? file.name : 'Select or drop project ZIP archive' }}
                                    </span>
                                    <span class="cb-upload-sub">
                                        Accepts .zip archives containing project source code
                                    </span>
                                </label>

                                <input
                                    id="codebase"
                                    type="file"
                                    accept=".zip"
                                    class="al-visually-hidden"
                                    @change="handleFileChange"
                                />

                                <div class="cb-upload-actions">
                                    <button
                                        type="button"
                                        class="al-btn al-btn--primary"
                                        :disabled="loading || !file"
                                        @click="handleUpload"
                                    >
                                        <span v-if="loading" class="al-spinner" role="status" aria-label="Scanning…"></span>
                                        <span v-else>Scan & Map Project</span>
                                    </button>
                                </div>
                            </div>

                            <div v-if="error" class="al-status-error" role="alert">
                                {{ error }}
                            </div>
                        </div>
                    </div>
                </section>

                <!-- When no project is loaded: Empty State -->
                <div v-if="!files.length && !loading" class="al-empty-state cb-empty-hero">
                    <div class="al-empty-state__icon" aria-hidden="true">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                            <rect x="3" y="3" width="7" height="7" rx="1.5" stroke="currentColor" stroke-width="1.4"/>
                            <rect x="14" y="3" width="7" height="7" rx="1.5" stroke="currentColor" stroke-width="1.4"/>
                            <rect x="8.5" y="14" width="7" height="7" rx="1.5" stroke="currentColor" stroke-width="1.4"/>
                        </svg>
                    </div>
                    <div class="al-empty-state__title">PROJECT NOT LOADED</div>
                    <p class="al-empty-state__desc">
                        Upload a ZIP project archive above to begin exploring its structure, file relationships, and architectural queries.
                    </p>
                </div>

                <!-- Step 2: Project Structure & Query (Shown when files are scanned) -->
                <template v-if="files.length">

                    <div class="al-workspace al-workspace--natural" style="margin-top: var(--space-8)">

                        <!-- Left Column: File Explorer Panel -->
                        <section class="al-workspace__panel" aria-labelledby="files-heading">
                            <div class="al-workspace__panel-header">
                                <span id="files-heading">PROJECT FILES</span>
                                <span class="file-count-badge">{{ filteredFiles.length }} / {{ files.length }}</span>
                            </div>

                            <div class="al-workspace__panel-body">
                                <div class="al-form-group">
                                    <input
                                        v-model="fileFilter"
                                        type="text"
                                        class="al-input al-input--sm"
                                        placeholder="Filter files by path…"
                                        aria-label="Filter project files"
                                    />
                                </div>

                                <ul class="cb-file-list" role="list">
                                    <li
                                        v-for="item in filteredFiles"
                                        :key="item.path"
                                        class="cb-file-item"
                                    >
                                        <svg width="14" height="14" viewBox="0 0 16 16" fill="none" class="cb-file-icon" aria-hidden="true">
                                            <path d="M3 2.5h7l3 3V13a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1z" stroke="currentColor" stroke-width="1.3"/>
                                            <path d="M10 2.5V6h3.5" stroke="currentColor" stroke-width="1.2"/>
                                        </svg>
                                        <code class="cb-file-path" :title="item.path">{{ item.path }}</code>
                                    </li>
                                </ul>
                            </div>
                        </section>

                        <!-- Right Column: Query & Answer Panel -->
                        <section class="al-workspace__panel" aria-labelledby="query-heading">
                            <div class="al-workspace__panel-header">
                                <span id="query-heading">ASK YOUR CODEBASE</span>
                            </div>

                            <div class="al-workspace__panel-body">
                                <form @submit.prevent="handleAnalyze" novalidate>
                                    <div class="al-form-group">
                                        <label for="codebase-query" class="al-label">
                                            <span>Architectural or Logic Query</span>
                                            <span class="field-required">*</span>
                                        </label>
                                        <textarea
                                            id="codebase-query"
                                            v-model="query"
                                            class="al-textarea"
                                            placeholder="e.g. Where is session authentication handled and how are credentials validated?"
                                            rows="4"
                                            required
                                        ></textarea>
                                    </div>

                                    <!-- Query Suggestions -->
                                    <div class="cb-suggestions">
                                        <span class="cb-sugg-label">Try:</span>
                                        <button
                                            type="button"
                                            class="cb-sugg-chip"
                                            @click="loadSuggestedQuery('Where is authentication and session management handled?')"
                                        >
                                            Auth flow
                                        </button>
                                        <button
                                            type="button"
                                            class="cb-sugg-chip"
                                            @click="loadSuggestedQuery('How is database connection and models configured?')"
                                        >
                                            DB Models
                                        </button>
                                        <button
                                            type="button"
                                            class="cb-sugg-chip"
                                            @click="loadSuggestedQuery('Where are API routes registered and exposed?')"
                                        >
                                            API Routes
                                        </button>
                                    </div>

                                    <button
                                        type="submit"
                                        class="al-btn al-btn--primary"
                                        :disabled="analyzing || !query.trim()"
                                        style="margin-top: 16px; width: 100%; justify-content: center"
                                    >
                                        <span v-if="analyzing" class="al-spinner" role="status" aria-label="Analyzing…"></span>
                                        <span v-else>Analyze Codebase</span>
                                        <svg v-if="!analyzing" aria-hidden="true" class="al-btn__arrow" width="16" height="16" viewBox="0 0 16 16" fill="none">
                                            <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                                        </svg>
                                    </button>
                                </form>

                                <!-- Analysis Result -->
                                <div v-if="analysis" class="al-result" style="margin-top: var(--space-4); border: 1px solid var(--border); border-radius: var(--radius-md)" role="region" aria-label="Codebase answer">
                                    <div class="al-result__section">
                                        <span class="al-result__label">Answer</span>
                                        <p class="al-result__value">{{ analysis.answer }}</p>
                                    </div>

                                    <div v-if="analysis.files?.length" class="al-result__section">
                                        <span class="al-result__label">Relevant Files & Functions</span>
                                        <ul class="al-result__list cb-relevant-list">
                                            <li v-for="rf in analysis.files" :key="rf.path">
                                                <code class="cb-relevant-path">{{ rf.path }}</code>
                                                <p class="cb-relevant-reason">{{ rf.reason }}</p>
                                            </li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </section>

                    </div>

                    <!-- Step 3: Implementation Topology Map -->
                    <div style="margin-top: var(--space-8)">
                        <ImplementationMap
                            :files="files"
                            :relationships="relationships"
                            title="Codebase Module Relationships"
                        />
                    </div>

                </template>

            </div>
        </main>
    </div>
</template>

<style scoped>
.cb-section {
    margin-bottom: var(--space-6);
}

.cb-loaded-badge {
    font-family: var(--mono);
    font-size: 0.7rem;
    font-weight: 700;
    color: var(--accent);
    padding: 2px 6px;
    background: var(--accent-soft);
    border-radius: var(--radius-sm);
}

.cb-upload-zone {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border: 2px dashed var(--border);
    border-radius: var(--radius-md);
    padding: var(--space-8) var(--space-6);
    background: var(--surface-alt);
    text-align: center;
    transition: border-color var(--duration-fast);
}

.cb-upload-zone:hover {
    border-color: var(--accent);
}

.cb-file-label {
    cursor: pointer;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--space-2);
}

.cb-upload-icon {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: var(--surface);
    border: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--accent);
    margin-bottom: var(--space-2);
}

.cb-upload-main {
    font-family: var(--heading);
    font-size: 1.05rem;
    font-weight: 600;
    color: var(--text-h);
}

.cb-upload-sub {
    font-size: 0.8rem;
    color: var(--text-muted);
}

.cb-upload-actions {
    margin-top: var(--space-5);
}

.cb-empty-hero {
    margin: var(--space-12) 0;
}

.file-count-badge {
    font-family: var(--mono);
    font-size: 0.7rem;
    color: var(--text-muted);
}

.cb-file-list {
    list-style: none;
    margin: 0;
    padding: 0;
    max-height: 380px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.cb-file-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 5px 8px;
    border-radius: var(--radius-sm);
    transition: background 0.15s;
    min-width: 0;
}

.cb-file-item:hover {
    background: var(--surface-alt);
}

.cb-file-icon {
    color: var(--text-muted);
    flex-shrink: 0;
}

.cb-file-path {
    font-size: 0.775rem;
    color: var(--text-h);
    background: none;
    border: none;
    padding: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    word-break: break-all;
}

.cb-suggestions {
    display: flex;
    align-items: center;
    gap: 6px;
    flex-wrap: wrap;
    margin-top: var(--space-2);
}

.cb-sugg-label {
    font-family: var(--mono);
    font-size: 0.7rem;
    color: var(--text-muted);
}

.cb-sugg-chip {
    font-family: var(--mono);
    font-size: 0.7rem;
    padding: 2px 7px;
    background: var(--surface-alt);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    color: var(--text-h);
    cursor: pointer;
    transition: background 0.15s;
}

.cb-sugg-chip:hover {
    background: var(--accent-soft);
    border-color: var(--accent);
    color: var(--accent);
}

.cb-relevant-list {
    list-style: none;
    padding-left: 0;
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
}

.cb-relevant-path {
    display: block;
    margin-bottom: 2px;
    font-weight: 600;
}

.cb-relevant-reason {
    font-size: 0.825rem;
    color: var(--text-muted);
    line-height: 1.45;
    margin: 0;
}
</style>