<script setup>
import { ref, computed, watch } from 'vue';
import ImplementationMap from '../components/ImplementationMap.vue';
import Navbar from '../components/Navbar.vue';
import MarkdownRenderer from '../components/MarkdownRenderer.vue';
import CodeBlock from '../components/CodeBlock.vue';
import {
    uploadCodebase,
    importGithubRepo,
    analyzeCodebase,
    getCodebaseFile,
    explainCodebaseCode
} from '../services/api';
import { tokenizeCode, detectLanguageFromPath } from '../services/highlighter';

const file = ref(null);
const files = ref([]);
const loading = ref(false);
const importing = ref(false);
const githubUrl = ref('');
const error = ref('');
const codebaseId = ref(null);

// Right column tab: 'inspector' | 'query'
const activeTab = ref('inspector');

// Query state (Ask Whole Codebase)
const query = ref('');
const analysis = ref(null);
const analyzing = ref(false);
const relationships = ref([]);
const fileFilter = ref('');
const copied = ref(false);

// File Viewer & Explain state
const selectedFile = ref(null);
const fileLoading = ref(false);
const startLine = ref(null);
const endLine = ref(null);
const tokenizedLines = ref([]);
const explaining = ref(false);
const explainError = ref('');
const explanation = ref(null);
const explainCopied = ref(false);

const filteredFiles = computed(() => {
    if (!fileFilter.value.trim()) return files.value;
    const q = fileFilter.value.toLowerCase();
    return files.value.filter(f => f.path.toLowerCase().includes(q));
});

const selectedCode = computed(() => {
    if (!selectedFile.value?.lines || startLine.value === null) return '';
    const total = selectedFile.value.lines.length;
    const start = Math.max(1, Math.min(total, startLine.value));
    const end = Math.max(start, Math.min(total, endLine.value || start));
    return selectedFile.value.lines.slice(start - 1, end).join('\n');
});

const hasSelection = computed(() => {
    return startLine.value !== null && endLine.value !== null;
});

const selectionCount = computed(() => {
    if (!hasSelection.value || !selectedFile.value?.lines) return 0;
    const total = selectedFile.value.lines.length;
    const start = Math.max(1, Math.min(total, startLine.value));
    const end = Math.max(start, Math.min(total, endLine.value || start));
    return end - start + 1;
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
        codebaseId.value = data.id || null;
        files.value = data.files || [];
        relationships.value = data.relationships || [];
        if (files.value.length > 0) {
            handleSelectFile(files.value[0]);
        }
    } catch (err) {
        error.value = err.message || 'Failed to scan and unpack codebase archive.';
    } finally {
        loading.value = false;
    }
}

async function handleGithubImport() {
    if (!githubUrl.value.trim()) {
        error.value = 'Please enter a public GitHub repository URL.';
        return;
    }

    importing.value = true;
    error.value = '';

    try {
        const data = await importGithubRepo(githubUrl.value.trim());
        codebaseId.value = data.id || null;
        files.value = data.files || [];
        relationships.value = data.relationships || [];
        if (files.value.length > 0) {
            handleSelectFile(files.value[0]);
        }
    } catch (err) {
        error.value = err.message || 'Failed to import GitHub repository.';
    } finally {
        importing.value = false;
    }
}

async function handleSelectFile(item) {
    if (selectedFile.value?.path === item.path && selectedFile.value?.content !== undefined) {
        activeTab.value = 'inspector';
        return;
    }

    fileLoading.value = true;
    explainError.value = '';
    explanation.value = null;
    startLine.value = null;
    endLine.value = null;
    activeTab.value = 'inspector';

    try {
        const fileData = await getCodebaseFile(item.path, codebaseId.value);
        const content = fileData.content || '';
        const lines = content.split('\n');
        const lang = detectLanguageFromPath(fileData.path);

        selectedFile.value = {
            path: fileData.path,
            size: fileData.size,
            content: content,
            lines: lines,
            lang: lang
        };

        // Asynchronously tokenize the file with Shiki
        tokenizeCode(content, lang).then(tokens => {
            tokenizedLines.value = tokens;
        });
    } catch (err) {
        explainError.value = err.message || 'Failed to load file content.';
    } finally {
        fileLoading.value = false;
    }
}

function handleLineClick(lineNum, event) {
    if (event?.shiftKey && startLine.value !== null) {
        const prev = startLine.value;
        startLine.value = Math.min(prev, lineNum);
        endLine.value = Math.max(prev, lineNum);
    } else {
        startLine.value = lineNum;
        endLine.value = lineNum;
    }
}

function clearSelection() {
    startLine.value = null;
    endLine.value = null;
}

function selectAllLines() {
    if (!selectedFile.value?.lines) return;
    startLine.value = 1;
    endLine.value = selectedFile.value.lines.length;
}

function handleStartLineInput(event) {
    const val = parseInt(event.target.value, 10);
    if (isNaN(val) || val < 1) {
        startLine.value = null;
        return;
    }
    const maxLine = selectedFile.value?.lines?.length || val;
    startLine.value = Math.min(val, maxLine);
    if (endLine.value === null || endLine.value < startLine.value) {
        endLine.value = startLine.value;
    }
}

function handleEndLineInput(event) {
    const val = parseInt(event.target.value, 10);
    if (isNaN(val) || val < 1) {
        endLine.value = null;
        return;
    }
    const maxLine = selectedFile.value?.lines?.length || val;
    endLine.value = Math.min(val, maxLine);
    if (startLine.value === null || startLine.value > endLine.value) {
        startLine.value = Math.min(1, endLine.value);
    }
}

function isLineSelected(lineNum) {
    if (startLine.value === null || endLine.value === null) return false;
    return lineNum >= startLine.value && lineNum <= endLine.value;
}

async function handleExplainFile() {
    if (!selectedFile.value) return;
    explaining.value = true;
    explainError.value = '';
    explanation.value = null;

    try {
        const result = await explainCodebaseCode({
            scope: 'file',
            file_path: selectedFile.value.path,
            codebase_id: codebaseId.value
        });
        explanation.value = result;
    } catch (err) {
        explainError.value = err.message || 'Failed to explain file.';
    } finally {
        explaining.value = false;
    }
}

async function handleExplainSelection() {
    if (!selectedFile.value || startLine.value === null) return;
    explaining.value = true;
    explainError.value = '';
    explanation.value = null;

    const sLine = Math.max(1, startLine.value);
    const eLine = Math.min(selectedFile.value.lines.length, endLine.value || sLine);

    try {
        const result = await explainCodebaseCode({
            scope: 'selection',
            file_path: selectedFile.value.path,
            start_line: sLine,
            end_line: eLine,
            code: selectedCode.value,
            codebase_id: codebaseId.value
        });
        explanation.value = result;
    } catch (err) {
        explainError.value = err.message || 'Failed to explain code selection.';
    } finally {
        explaining.value = false;
    }
}

function getExplanationAiMarkdown() {
    if (!explanation.value) return '';
    const exp = explanation.value;
    const parts = [];

    if (exp.scope === 'selection') {
        parts.push(
            `# ArrowLens Code Explanation: \`${exp.file_path}\` (Lines ${exp.start_line}–${exp.end_line})`,
            '',
            '## Selected Code',
            '```',
            exp.selected_code || selectedCode.value || '',
            '```',
            '',
            '## What It Does',
            exp.what_it_does || '',
            '',
            '## How It Works',
            exp.how_it_works || '',
            '',
            '## Why It Exists',
            exp.why_it_exists || '',
            '',
            '## Dependencies & Context',
            exp.dependencies_context || '',
            '',
            '## Modification Considerations & Invariants',
            exp.modification_notes || ''
        );
    } else {
        parts.push(
            `# ArrowLens File Architecture Explanation: \`${exp.file_path}\``,
            '',
            '## Purpose',
            exp.purpose || '',
            '',
            '## What It Does',
            exp.what_it_does || '',
            ''
        );
        if (exp.dependencies && exp.dependencies.length) {
            parts.push('## Key Dependencies');
            if (Array.isArray(exp.dependencies)) {
                exp.dependencies.forEach(d => parts.push(`- ${d}`));
            } else {
                parts.push(`- ${exp.dependencies}`);
            }
            parts.push('');
        }
        parts.push(
            '## Inputs & Outputs',
            exp.inputs_outputs || '',
            '',
            '## Codebase Architecture Fit',
            exp.architecture_fit || '',
            '',
            '## Important Considerations for Modification',
            exp.modification_notes || ''
        );
    }
    return parts.join('\n');
}

async function copyExplanationForAi() {
    const text = getExplanationAiMarkdown();
    if (!text) return;

    try {
        await navigator.clipboard.writeText(text);
        explainCopied.value = true;
        setTimeout(() => {
            explainCopied.value = false;
        }, 2000);
    } catch (e) {
        console.error('Clipboard copy failed:', e);
    }
}

// Global Query handling
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

function getCodebaseAiMarkdown() {
    if (!analysis.value) return '';
    const parts = [
        '# ArrowLens Codebase Analysis',
        '',
        '## Question',
        query.value || 'Codebase Architectural Query',
        '',
        '## Answer',
        analysis.value.answer || ''
    ];

    if (analysis.value.files?.length) {
        parts.push('', '## Relevant Files');
        analysis.value.files.forEach(f => {
            parts.push(`- \`${f.path}\` — ${f.reason}`);
        });
    }

    if (relationships.value?.length) {
        parts.push('', '## Implementation Relationships');
        relationships.value.forEach(rel => {
            parts.push(`- \`${rel.source}\` → \`${rel.target}\``);
        });
    }

    return parts.join('\n');
}

async function copyForAi() {
    const text = getCodebaseAiMarkdown();
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
                        <span class="al-lens-eyebrow__icon al-lens-eyebrow__icon--codebase" aria-hidden="true">
                            <svg width="13" height="13" viewBox="0 0 16 16" fill="none">
                                <rect x="2" y="2.5" width="5" height="4" rx="1" stroke="currentColor" stroke-width="1.3"/>
                                <rect x="9" y="2.5" width="5" height="4" rx="1" stroke="currentColor" stroke-width="1.3"/>
                                <rect x="5.5" y="9.5" width="5" height="4" rx="1" stroke="currentColor" stroke-width="1.3"/>
                                <path d="M4.5 6.5v1.5a1 1 0 0 0 1 1h5a1 1 0 0 0 1-1V6.5" stroke="currentColor" stroke-width="1.2"/>
                            </svg>
                        </span>
                        <span>CODEBASE LENS</span>
                    </div>
                    <h1 class="al-page-title">Codebase Topology & File Inspector</h1>
                    <p class="al-page-desc">
                        Explore syntax-highlighted source code, select line ranges, generate focused AI explanations, query overall architecture boundaries, and map module AST relationships.
                    </p>
                </header>

                <!-- Step 1: Upload Archive / Import GitHub Section -->
                <section class="cb-section" aria-labelledby="upload-heading">
                    <div class="al-lens-panel" style="min-height: auto">
                        <div class="al-lens-panel__header">
                            <div class="al-lens-panel__title">
                                <span id="upload-heading">STEP 01 // LOAD REPOSITORY</span>
                            </div>
                            <span v-if="files.length" class="cb-loaded-badge">
                                {{ files.length }} Files Indexed
                            </span>
                        </div>

                        <div class="al-lens-panel__body">
                            <div class="cb-load-methods">

                                <!-- Option A: ZIP Archive Upload -->
                                <div class="cb-method-card">
                                    <span class="cb-method-tag">OPTION A // ZIP ARCHIVE</span>
                                    <div class="cb-upload-zone">
                                        <label for="codebase" class="cb-file-label">
                                            <div class="cb-upload-icon" aria-hidden="true">
                                                <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
                                                    <path d="M12 4v12M8 8l4-4 4 4M4 17v2a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-2" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
                                                </svg>
                                            </div>
                                            <span class="cb-upload-main">
                                                {{ file ? file.name : 'Select or drop project ZIP archive' }}
                                            </span>
                                            <span class="cb-upload-sub">
                                                Accepts .zip archives containing source code
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
                                                :disabled="loading || importing || !file"
                                                @click="handleUpload"
                                            >
                                                <span v-if="loading" class="al-spinner" role="status" aria-label="Scanning…"></span>
                                                <span v-else>Scan & Map Project</span>
                                            </button>
                                        </div>
                                    </div>
                                </div>

                                <!-- Option B: Public GitHub Repository Import -->
                                <div class="cb-method-card">
                                    <span class="cb-method-tag">OPTION B // PUBLIC GITHUB</span>
                                    <div class="cb-github-zone">
                                        <div class="cb-github-icon" aria-hidden="true">
                                            <svg width="24" height="24" viewBox="0 0 16 16" fill="currentColor">
                                                <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
                                            </svg>
                                        </div>

                                        <div class="al-form-group cb-github-form-group">
                                            <label for="github-repo-url" class="al-label">
                                                <span>GitHub Repository</span>
                                            </label>
                                            <input
                                                id="github-repo-url"
                                                v-model="githubUrl"
                                                type="url"
                                                class="al-input"
                                                placeholder="https://github.com/user/repository"
                                                :disabled="loading || importing"
                                                @keyup.enter="handleGithubImport"
                                            />
                                        </div>

                                        <div class="cb-upload-actions" style="width: 100%">
                                            <button
                                                type="button"
                                                class="al-btn al-btn--primary"
                                                style="width: 100%; justify-content: center"
                                                :disabled="importing || loading || !githubUrl.trim()"
                                                @click="handleGithubImport"
                                            >
                                                <span v-if="importing" class="al-spinner" role="status" aria-label="Importing repository…"></span>
                                                <span v-else>Import Repository</span>
                                            </button>
                                        </div>
                                    </div>
                                </div>

                            </div>

                            <div v-if="error" class="al-status-error" role="alert" style="margin-top: 16px">
                                <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true" style="flex-shrink: 0; margin-top: 2px">
                                    <circle cx="8" cy="8" r="7" stroke="currentColor" stroke-width="1.3"/>
                                    <path d="M8 5v3.5M8 11v.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                                </svg>
                                <span>{{ error }}</span>
                            </div>
                        </div>
                    </div>
                </section>

                <!-- Importing Loading State -->
                <div v-if="importing" class="al-loading-state cb-empty-hero" role="status" aria-live="polite">
                    <div class="al-spinner"></div>
                    <span class="loading-title">IMPORTING REPOSITORY</span>
                    <span class="loading-sub">Downloading public GitHub archive and mapping AST structure…</span>
                </div>

                <!-- When no project is loaded: Empty State -->
                <div v-else-if="!files.length && !loading" class="al-empty-state cb-empty-hero">
                    <div class="al-empty-state__icon" aria-hidden="true">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                            <rect x="3" y="3" width="7" height="7" rx="1.5" stroke="currentColor" stroke-width="1.4"/>
                            <rect x="14" y="3" width="7" height="7" rx="1.5" stroke="currentColor" stroke-width="1.4"/>
                            <rect x="8.5" y="14" width="7" height="7" rx="1.5" stroke="currentColor" stroke-width="1.4"/>
                        </svg>
                    </div>
                    <div class="al-empty-state__title">PROJECT NOT LOADED</div>
                    <p class="al-empty-state__desc">
                        Upload a ZIP project archive or import a public GitHub repository above to begin exploring its source code, line-level explanations, and architectural relationships.
                    </p>
                </div>

                <!-- Step 2: Project Workspace (File Explorer + Code Viewer / Explain / Query) -->
                <template v-if="files.length">

                    <div class="al-lens-workspace" style="margin-top: var(--space-8)">

                        <!-- Left Column: File Explorer Panel -->
                        <section class="al-lens-panel" aria-labelledby="files-heading">
                            <div class="al-lens-panel__header">
                                <div class="al-lens-panel__title">
                                    <span id="files-heading">PROJECT FILES</span>
                                </div>
                                <span class="file-count-badge">{{ filteredFiles.length }} / {{ files.length }}</span>
                            </div>

                            <div class="al-lens-panel__body">
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
                                        :class="{ 'cb-file-item--active': selectedFile?.path === item.path }"
                                        @click="handleSelectFile(item)"
                                        role="button"
                                        tabindex="0"
                                        @keydown.enter="handleSelectFile(item)"
                                        @keydown.space.prevent="handleSelectFile(item)"
                                        :aria-selected="selectedFile?.path === item.path"
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

                        <!-- Right Column: Code Viewer & AI Analysis Panel -->
                        <section class="al-lens-panel" aria-labelledby="workspace-heading">
                            <!-- Dual Tab Header -->
                            <div class="al-lens-panel__header cb-tabs-header">
                                <div class="cb-tabs-nav" role="tablist" aria-label="Codebase Views">
                                    <button
                                        type="button"
                                        role="tab"
                                        :aria-selected="activeTab === 'inspector'"
                                        class="cb-tab-btn"
                                        :class="{ 'cb-tab-btn--active': activeTab === 'inspector' }"
                                        @click="activeTab = 'inspector'"
                                    >
                                        <svg width="13" height="13" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                                            <path d="M2 3h12v10H2z" stroke="currentColor" stroke-width="1.3" rx="1"/>
                                            <path d="M5 6l2 2-2 2M9 10h2" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
                                        </svg>
                                        <span>File Inspector & Explain</span>
                                    </button>
                                    <button
                                        type="button"
                                        role="tab"
                                        :aria-selected="activeTab === 'query'"
                                        class="cb-tab-btn"
                                        :class="{ 'cb-tab-btn--active': activeTab === 'query' }"
                                        @click="activeTab = 'query'"
                                    >
                                        <svg width="13" height="13" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                                            <circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="1.3"/>
                                            <path d="M6 6.5a2 2 0 1 1 3 1.7c-.5.3-.8.7-.8 1.3v.5M8 12.5v.5" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
                                        </svg>
                                        <span>Ask Codebase</span>
                                    </button>
                                </div>

                                <button
                                    v-if="activeTab === 'inspector' && explanation"
                                    type="button"
                                    class="al-btn-copy-ai"
                                    :class="{ 'al-btn-copy-ai--copied': explainCopied }"
                                    @click="copyExplanationForAi"
                                    aria-label="Copy code explanation formatted for AI assistant"
                                >
                                    <svg v-if="!explainCopied" width="13" height="13" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                                        <rect x="5" y="5" width="8" height="8" rx="1.5" stroke="currentColor" stroke-width="1.3"/>
                                        <path d="M3 11V3.5A1.5 1.5 0 0 1 4.5 2H11" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
                                    </svg>
                                    <svg v-else width="13" height="13" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                                        <path d="M3.5 8.5L6.5 11.5L12.5 4.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                                    </svg>
                                    <span>{{ explainCopied ? 'Copied' : 'Copy for AI' }}</span>
                                </button>

                                <button
                                    v-else-if="activeTab === 'query' && analysis"
                                    type="button"
                                    class="al-btn-copy-ai"
                                    :class="{ 'al-btn-copy-ai--copied': copied }"
                                    @click="copyForAi"
                                    aria-label="Copy codebase analysis formatted for AI assistant"
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

                            <div class="al-lens-panel__body">

                                <!-- TAB 1: FILE INSPECTOR & EXPLAIN -->
                                <div v-if="activeTab === 'inspector'">

                                    <!-- Loading file -->
                                    <div v-if="fileLoading" class="al-loading-state" style="padding: var(--space-8) 0" role="status">
                                        <div class="al-spinner"></div>
                                        <span class="loading-sub">Loading file contents…</span>
                                    </div>

                                    <!-- No file selected -->
                                    <div v-else-if="!selectedFile" class="cb-no-file-prompt">
                                        <svg width="24" height="24" viewBox="0 0 16 16" fill="none" aria-hidden="true" style="color: var(--text-muted)">
                                            <path d="M3 2.5h7l3 3V13a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1z" stroke="currentColor" stroke-width="1.3"/>
                                        </svg>
                                        <span>Select a file from the project explorer on the left to view source code and explain sections.</span>
                                    </div>

                                    <!-- Selected File View -->
                                    <div v-else class="cb-viewer-container">

                                        <!-- File Metadata Header -->
                                        <div class="cb-viewer-header">
                                            <div class="cb-viewer-path">
                                                <code :title="selectedFile.path">{{ selectedFile.path }}</code>
                                            </div>
                                            <div class="cb-viewer-meta">
                                                <span v-if="selectedFile.lang" class="cb-meta-tag">{{ selectedFile.lang }}</span>
                                                <span class="cb-meta-tag">{{ selectedFile.lines.length }} lines</span>
                                                <span v-if="selectedFile.size" class="cb-meta-tag">{{ Math.round(selectedFile.size / 1024) }} KB</span>
                                            </div>
                                        </div>

                                        <!-- Line Range Controls & Explain Action Toolbar -->
                                        <div class="cb-toolbar">
                                            <div class="cb-range-picker">
                                                <span class="cb-range-label">Lines:</span>
                                                <input
                                                    type="number"
                                                    class="al-input cb-line-input"
                                                    :value="startLine"
                                                    @input="handleStartLineInput"
                                                    placeholder="Start"
                                                    min="1"
                                                    :max="selectedFile.lines.length"
                                                    aria-label="Start line number"
                                                />
                                                <span class="cb-range-sep">to</span>
                                                <input
                                                    type="number"
                                                    class="al-input cb-line-input"
                                                    :value="endLine"
                                                    @input="handleEndLineInput"
                                                    placeholder="End"
                                                    min="1"
                                                    :max="selectedFile.lines.length"
                                                    aria-label="End line number"
                                                />

                                                <button
                                                    v-if="hasSelection"
                                                    type="button"
                                                    class="cb-btn-text"
                                                    @click="clearSelection"
                                                    title="Clear line selection"
                                                >
                                                    Clear
                                                </button>
                                                <button
                                                    type="button"
                                                    class="cb-btn-text"
                                                    @click="selectAllLines"
                                                    title="Select entire file"
                                                >
                                                    All
                                                </button>
                                            </div>

                                            <div class="cb-action-btns">
                                                <button
                                                    type="button"
                                                    class="al-btn al-btn--sm al-btn--outline"
                                                    :disabled="explaining"
                                                    @click="handleExplainFile"
                                                    title="Explain entire file structure and purpose"
                                                >
                                                    <span v-if="explaining && !hasSelection" class="al-spinner" role="status"></span>
                                                    <span>Explain File</span>
                                                </button>

                                                <button
                                                    type="button"
                                                    class="al-btn al-btn--sm al-btn--primary"
                                                    :disabled="explaining || !hasSelection"
                                                    @click="handleExplainSelection"
                                                    :title="hasSelection ? `Explain lines ${startLine} to ${endLine}` : 'Select line range to explain'"
                                                >
                                                    <span v-if="explaining && hasSelection" class="al-spinner" role="status"></span>
                                                    <span>{{ hasSelection ? `Explain Selection (${selectionCount} lines)` : 'Explain Selection' }}</span>
                                                </button>
                                            </div>
                                        </div>

                                        <!-- Code Viewer Box with Shiki Highlighted Tokens -->
                                        <div class="cb-code-box" role="region" :aria-label="`Source code for ${selectedFile.path}`" tabindex="0">
                                            <div class="cb-code-scroll">
                                                <div
                                                    v-for="(codeLine, idx) in selectedFile.lines"
                                                    :key="idx"
                                                    class="cb-code-row"
                                                    :class="{ 'cb-code-row--selected': isLineSelected(idx + 1) }"
                                                >
                                                    <span
                                                        class="cb-line-num"
                                                        @click="handleLineClick(idx + 1, $event)"
                                                        :title="`Click to select line ${idx + 1} (Shift-click to select range)`"
                                                    >
                                                        {{ idx + 1 }}
                                                    </span>

                                                    <!-- Shiki syntax highlighted tokens if ready -->
                                                    <span v-if="tokenizedLines && tokenizedLines[idx]" class="cb-line-text">
                                                        <span
                                                            v-for="(tok, tIdx) in tokenizedLines[idx]"
                                                            :key="tIdx"
                                                            :style="{ color: tok.color, fontStyle: tok.fontStyle ? 'italic' : 'normal' }"
                                                        >{{ tok.content }}</span>
                                                    </span>

                                                    <!-- Plain fallback -->
                                                    <span v-else class="cb-line-text">{{ codeLine || ' ' }}</span>
                                                </div>
                                            </div>
                                        </div>

                                        <!-- Explain Error Banner -->
                                        <div v-if="explainError" class="al-status-error" role="alert" style="margin-top: var(--space-4)">
                                            <span>{{ explainError }}</span>
                                        </div>

                                        <!-- Explaining Loading State -->
                                        <div v-if="explaining" class="al-loading-state" style="margin-top: var(--space-4); padding: var(--space-6)" role="status">
                                            <div class="al-spinner"></div>
                                            <span class="loading-sub">Analyzing code with Gemini…</span>
                                        </div>

                                        <!-- Explanation Result Card -->
                                        <div
                                            v-if="explanation && !explaining"
                                            class="al-lens-artifact cb-explain-result"
                                            role="region"
                                            aria-label="Code explanation"
                                        >
                                            <div class="cb-explain-header">
                                                <span class="cb-explain-badge">
                                                    {{ explanation.scope === 'selection' ? `LINES ${explanation.start_line}–${explanation.end_line} EXPLANATION` : 'FILE ARCHITECTURE EXPLANATION' }}
                                                </span>
                                            </div>

                                            <!-- File Scope Fields -->
                                            <template v-if="explanation.scope === 'file'">
                                                <div class="al-result__section">
                                                    <span class="al-result__label">Core Purpose</span>
                                                    <MarkdownRenderer :content="explanation.purpose" class="cb-explain-lead" />
                                                </div>

                                                <div class="al-result__section">
                                                    <span class="al-result__label">What This File Does</span>
                                                    <MarkdownRenderer :content="explanation.what_it_does" class="al-result__value" />
                                                </div>

                                                <div v-if="explanation.dependencies?.length" class="al-result__section">
                                                    <span class="al-result__label">Key Dependencies</span>
                                                    <ul class="cb-deps-list">
                                                        <li v-for="(dep, dIdx) in (Array.isArray(explanation.dependencies) ? explanation.dependencies : [explanation.dependencies])" :key="dIdx">
                                                            <code>{{ dep }}</code>
                                                        </li>
                                                    </ul>
                                                </div>

                                                <div v-if="explanation.inputs_outputs" class="al-result__section">
                                                    <span class="al-result__label">Inputs & Outputs / Exported Symbols</span>
                                                    <MarkdownRenderer :content="explanation.inputs_outputs" class="al-result__value" />
                                                </div>

                                                <div v-if="explanation.architecture_fit" class="al-result__section">
                                                    <span class="al-result__label">Codebase Architecture Fit</span>
                                                    <MarkdownRenderer :content="explanation.architecture_fit" class="al-result__value" />
                                                </div>

                                                <div v-if="explanation.modification_notes" class="cb-caution-box">
                                                    <span class="cb-caution-label">Considerations Before Modifying</span>
                                                    <MarkdownRenderer :content="explanation.modification_notes" class="cb-caution-text" />
                                                </div>
                                            </template>

                                            <!-- Selection Scope Fields -->
                                            <template v-else>
                                                <div class="al-result__section">
                                                    <span class="al-result__label">What This Section Does</span>
                                                    <MarkdownRenderer :content="explanation.what_it_does" class="cb-explain-lead" />
                                                </div>

                                                <div v-if="explanation.how_it_works" class="al-result__section">
                                                    <span class="al-result__label">How It Works (Logic Breakdown)</span>
                                                    <MarkdownRenderer :content="explanation.how_it_works" class="al-result__value" />
                                                </div>

                                                <div v-if="explanation.why_it_exists" class="al-result__section">
                                                    <span class="al-result__label">Why It Exists</span>
                                                    <MarkdownRenderer :content="explanation.why_it_exists" class="al-result__value" />
                                                </div>

                                                <div v-if="explanation.dependencies_context" class="al-result__section">
                                                    <span class="al-result__label">Dependencies & Context Relied Upon</span>
                                                    <MarkdownRenderer :content="explanation.dependencies_context" class="al-result__value" />
                                                </div>

                                                <div v-if="explanation.modification_notes" class="cb-caution-box">
                                                    <span class="cb-caution-label">Considerations & Invariants Before Editing</span>
                                                    <MarkdownRenderer :content="explanation.modification_notes" class="cb-caution-text" />
                                                </div>
                                            </template>
                                        </div>

                                    </div>

                                </div>

                                <!-- TAB 2: ASK WHOLE CODEBASE -->
                                <div v-else-if="activeTab === 'query'">
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
                                    <div v-if="analysis" class="al-lens-artifact al-result" style="margin-top: var(--space-4); border: 1px solid var(--border); border-radius: var(--radius-md)" role="region" aria-label="Codebase answer">
                                        <div class="al-result__section">
                                            <span class="al-result__label">Answer</span>
                                            <MarkdownRenderer :content="analysis.answer" class="al-result__value" />
                                        </div>

                                        <div v-if="analysis.files?.length" class="al-result__section">
                                            <span class="al-result__label">Relevant Files & Functions</span>
                                            <ul class="al-result__list cb-relevant-list">
                                                <li v-for="rf in analysis.files" :key="rf.path">
                                                    <code class="cb-relevant-path">{{ rf.path }}</code>
                                                    <MarkdownRenderer :content="rf.reason" inline class="cb-relevant-reason" />
                                                </li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>

                            </div>
                        </section>

                    </div>

                    <!-- Step 3: Implementation Topology Map (Full-Width Secondary Artifact) -->
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

.cb-load-methods {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--space-5);
}

@media (max-width: 768px) {
    .cb-load-methods {
        grid-template-columns: 1fr;
    }
}

.cb-method-card {
    display: flex;
    flex-direction: column;
    gap: var(--space-2);
}

.cb-method-tag {
    font-family: var(--mono);
    font-size: 0.675rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: var(--text-muted);
}

.cb-upload-zone,
.cb-github-zone {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border: 1px dashed var(--border-strong);
    border-radius: var(--radius-md);
    padding: var(--space-6);
    background: var(--surface-alt);
    text-align: center;
    transition: border-color var(--duration-fast);
    min-height: 180px;
    box-sizing: border-box;
}

.cb-upload-zone:hover,
.cb-github-zone:focus-within {
    border-color: var(--accent);
}

.cb-file-label {
    cursor: pointer;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--space-2);
}

.cb-upload-icon,
.cb-github-icon {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: var(--surface);
    border: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--accent);
    margin-bottom: var(--space-1);
}

.cb-upload-main {
    font-family: var(--heading);
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--text-h);
}

.cb-upload-sub {
    font-size: 0.775rem;
    color: var(--text-muted);
}

.cb-upload-actions {
    margin-top: var(--space-4);
}

.cb-github-form-group {
    text-align: left;
    margin-bottom: var(--space-1);
}

.cb-empty-hero {
    margin: var(--space-12) 0;
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

.file-count-badge {
    font-family: var(--mono);
    font-size: 0.7rem;
    color: var(--text-muted);
}

.cb-file-list {
    list-style: none;
    margin: 0;
    padding: 0;
    max-height: 520px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 3px;
}

.cb-file-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 10px;
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition: background 0.15s, border-color 0.15s;
    min-width: 0;
    border: 1px solid transparent;
}

.cb-file-item:hover {
    background: var(--surface-alt);
}

.cb-file-item--active {
    background: var(--accent-soft);
    border-color: var(--accent);
}

.cb-file-item--active .cb-file-icon {
    color: var(--accent);
}

.cb-file-item--active .cb-file-path {
    color: var(--accent);
    font-weight: 600;
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

/* Tabs Header */
.cb-tabs-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--space-2);
    flex-wrap: wrap;
}

.cb-tabs-nav {
    display: flex;
    gap: 4px;
    background: var(--surface-alt);
    padding: 2px;
    border-radius: var(--radius-sm);
    border: 1px solid var(--border);
}

.cb-tab-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    font-family: var(--mono);
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--text-muted);
    background: transparent;
    border: none;
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition: all 0.15s;
}

.cb-tab-btn:hover {
    color: var(--text-h);
}

.cb-tab-btn--active {
    background: var(--surface);
    color: var(--accent);
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

/* Code Viewer & Toolbar */
.cb-no-file-prompt {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    gap: var(--space-2);
    padding: var(--space-10) var(--space-4);
    color: var(--text-muted);
    font-size: 0.85rem;
}

.cb-viewer-container {
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
}

.cb-viewer-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--space-2);
    background: var(--surface-alt);
    padding: 6px 10px;
    border-radius: var(--radius-sm);
    border: 1px solid var(--border);
}

.cb-viewer-path {
    min-width: 0;
    overflow: hidden;
}

.cb-viewer-path code {
    font-family: var(--mono);
    font-size: 0.775rem;
    font-weight: 600;
    color: var(--text-h);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    display: block;
}

.cb-viewer-meta {
    display: flex;
    align-items: center;
    gap: 6px;
    flex-shrink: 0;
}

.cb-meta-tag {
    font-family: var(--mono);
    font-size: 0.7rem;
    color: var(--text-muted);
    background: var(--surface);
    padding: 2px 6px;
    border-radius: var(--radius-sm);
    border: 1px solid var(--border);
}

.cb-toolbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--space-3);
    flex-wrap: wrap;
    background: var(--surface-alt);
    padding: 6px 10px;
    border-radius: var(--radius-sm);
    border: 1px solid var(--border);
}

.cb-range-picker {
    display: flex;
    align-items: center;
    gap: 6px;
}

.cb-range-label {
    font-family: var(--mono);
    font-size: 0.7rem;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
}

.cb-range-sep {
    font-family: var(--mono);
    font-size: 0.7rem;
    color: var(--text-muted);
}

.cb-line-input {
    width: 60px;
    padding: 2px 6px;
    font-family: var(--mono);
    font-size: 0.75rem;
    height: 26px;
    text-align: center;
}

.cb-btn-text {
    background: none;
    border: none;
    font-family: var(--mono);
    font-size: 0.7rem;
    color: var(--accent);
    cursor: pointer;
    text-decoration: underline;
    padding: 0 4px;
}

.cb-btn-text:hover {
    color: var(--text-h);
}

.cb-action-btns {
    display: flex;
    align-items: center;
    gap: 6px;
}

/* Monospace Code Box */
.cb-code-box {
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    background: #181c24;
    max-height: 380px;
    overflow: auto;
    font-family: var(--mono);
    font-size: 0.8rem;
    line-height: 1.5;
}

.cb-code-scroll {
    min-width: 100%;
    width: max-content;
}

.cb-code-row {
    display: flex;
    align-items: baseline;
    min-height: 22px;
    transition: background 0.1s;
}

.cb-code-row:hover {
    background: rgba(255, 255, 255, 0.04);
}

.cb-code-row--selected {
    background: rgba(59, 130, 246, 0.18) !important;
}

.cb-line-num {
    display: inline-block;
    width: 44px;
    min-width: 44px;
    padding: 0 10px 0 6px;
    text-align: right;
    color: var(--text-muted);
    user-select: none;
    cursor: pointer;
    font-size: 0.75rem;
    border-right: 1px solid var(--border);
    background: rgba(0, 0, 0, 0.2);
    opacity: 0.75;
}

.cb-line-num:hover {
    color: var(--accent);
    opacity: 1;
}

.cb-code-row--selected .cb-line-num {
    color: var(--accent);
    font-weight: 700;
    opacity: 1;
    border-right-color: var(--accent);
}

.cb-line-text {
    padding: 0 12px;
    white-space: pre;
    color: #e1e4e8;
}

/* Explanation Artifact */
.cb-explain-result {
    margin-top: var(--space-4);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: var(--space-4);
    background: var(--surface);
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
}

.cb-explain-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: var(--space-1);
}

.cb-explain-badge {
    font-family: var(--mono);
    font-size: 0.675rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: var(--accent);
    background: var(--accent-soft);
    padding: 2px 8px;
    border-radius: var(--radius-sm);
}

.cb-explain-lead {
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text-h);
    line-height: 1.5;
    margin: 0;
}

.cb-deps-list {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
}

.cb-deps-list code {
    font-family: var(--mono);
    font-size: 0.75rem;
    padding: 2px 6px;
    background: var(--surface-alt);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    color: var(--text-h);
}

.cb-caution-box {
    margin-top: var(--space-2);
    padding: var(--space-3);
    background: var(--surface-alt);
    border-left: 3px solid var(--accent);
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
}

.cb-caution-label {
    font-family: var(--mono);
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    color: var(--accent);
    display: block;
    margin-bottom: 2px;
}

.cb-caution-text {
    font-size: 0.825rem;
    color: var(--text-h);
    line-height: 1.45;
    margin: 0;
}

/* Global Query Styles */
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
    overflow-wrap: anywhere;
    word-break: break-all;
}

.cb-relevant-reason {
    font-size: 0.825rem;
    color: var(--text-muted);
    line-height: 1.45;
    margin: 0;
    overflow-wrap: anywhere;
}
</style>