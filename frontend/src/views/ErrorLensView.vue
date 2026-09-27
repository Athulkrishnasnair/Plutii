<script setup>
import { ref } from 'vue';
import { analyzeError } from '../services/api';
import Navbar from '../components/Navbar.vue';
import MarkdownRenderer from '../components/MarkdownRenderer.vue';

const error = ref('');
const code = ref('');
const context = ref('');

const result = ref(null);
const loading = ref(false);
const apiError = ref('');
const copied = ref(false);

function loadSample() {
    error.value = `Traceback (most recent call last):
  File "app/api/auth.py", line 48, in handle_session
    user_id = session['user_id']
KeyError: 'user_id'`;
    code.value = `def handle_session():
    user_id = session['user_id']
    user = db.session.get(User, user_id)
    return jsonify(user.to_dict())`;
    context.value = 'User attempted to access protected dashboard route without an active session cookie.';
}

function clearAll() {
    error.value = '';
    code.value = '';
    context.value = '';
    result.value = null;
    apiError.value = '';
}

async function handleAnalyze() {
    if (!error.value.trim()) return;
    loading.value = true;
    apiError.value = '';
    result.value = null;

    try {
        result.value = await analyzeError(error.value.trim(), code.value.trim(), context.value.trim());
    } catch (err) {
        apiError.value = err.message || 'ArrowLens could not analyze this error. Please verify your inputs and try again.';
    } finally {
        loading.value = false;
    }
}

function getErrorAiMarkdown() {
    if (!result.value) return '';
    const parts = [
        '# ArrowLens Error Analysis',
        '',
        '## Problem',
        result.value.problem || '',
        '',
        '## Likely Cause',
        result.value.cause || '',
        '',
        '## Suggested Fix',
        result.value.fix || '',
        '',
        '## Verification',
        ...(result.value.verification || []).map(v => `- ${v}`)
    ];

    if (error.value || code.value || context.value) {
        parts.push('', '## Original Context');
        if (error.value) {
            parts.push('', '```', error.value, '```');
        }
        if (code.value) {
            parts.push('', '```', code.value, '```');
        }
        if (context.value) {
            parts.push('', context.value);
        }
    }

    return parts.join('\n');
}

async function copyForAi() {
    const text = getErrorAiMarkdown();
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

                <!-- Page Header -->
                <header class="al-page-header al-lens-header">
                    <div class="al-lens-eyebrow">
                        <span class="al-lens-eyebrow__icon al-lens-eyebrow__icon--error" aria-hidden="true">
                            <svg width="13" height="13" viewBox="0 0 16 16" fill="none">
                                <path d="M8 2.2L14.2 13.5H1.8L8 2.2Z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/>
                                <path d="M8 6.2v3.3M8 11.2v.3" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
                            </svg>
                        </span>
                        <span>ERROR LENS</span>
                    </div>
                    <h1 class="al-page-title">Fault Isolation & Analysis</h1>
                    <p class="al-page-desc">
                        Paste an error message or stack trace. ArrowLens isolates the problem,
                        determines the root cause, generates a concrete fix, and specifies verification checks.
                    </p>
                </header>

                <div class="al-lens-workspace">

                    <!-- Left: Input Workspace Panel -->
                    <section class="al-lens-panel" aria-labelledby="input-heading">
                        <div class="al-lens-panel__header">
                            <div class="al-lens-panel__title">
                                <span id="input-heading">FAULT PAYLOAD</span>
                            </div>
                            <div class="panel-header-actions">
                                <button
                                    v-if="!error"
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
                            <form @submit.prevent="handleAnalyze" novalidate>
                                <div class="al-form-group">
                                    <label for="el-error" class="al-label">
                                        <span>Error Message or Traceback</span>
                                        <span class="field-required">*</span>
                                    </label>
                                    <textarea
                                        id="el-error"
                                        v-model="error"
                                        class="al-textarea al-textarea--mono"
                                        placeholder="Paste error output, exception traceback, or terminal log…"
                                        rows="6"
                                        required
                                        aria-required="true"
                                    ></textarea>
                                </div>

                                <div class="al-form-group" style="margin-top: 16px">
                                    <label for="el-code" class="al-label">
                                        <span>Relevant Code Snippet</span>
                                        <span class="label-optional">(optional)</span>
                                    </label>
                                    <textarea
                                        id="el-code"
                                        v-model="code"
                                        class="al-textarea al-textarea--mono"
                                        placeholder="Paste the function or file snippet where the error occurred…"
                                        rows="5"
                                    ></textarea>
                                </div>

                                <div class="al-form-group" style="margin-top: 16px">
                                    <label for="el-context" class="al-label">
                                        <span>Execution Context</span>
                                        <span class="label-optional">(optional)</span>
                                    </label>
                                    <textarea
                                        id="el-context"
                                        v-model="context"
                                        class="al-textarea"
                                        placeholder="What operation or environment condition triggered this error?"
                                        rows="2"
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
                                    :disabled="loading || !error.trim()"
                                    style="margin-top: 20px; width: 100%; justify-content: center"
                                >
                                    <span v-if="loading" class="al-spinner" role="status" aria-label="Analyzing…"></span>
                                    <span v-else>Analyze Error Signal</span>
                                    <svg v-if="!loading" aria-hidden="true" class="al-btn__arrow" width="16" height="16" viewBox="0 0 16 16" fill="none">
                                        <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                                    </svg>
                                </button>
                            </form>
                        </div>
                    </section>

                    <!-- Right: Analysis Result Panel -->
                    <section class="al-lens-panel" aria-labelledby="result-heading">
                        <div class="al-lens-panel__header">
                            <div class="al-lens-panel__title">
                                <span id="result-heading">GROUNDED SIGNAL</span>
                            </div>
                            <button
                                v-if="result"
                                type="button"
                                class="al-btn-copy-ai"
                                :class="{ 'al-btn-copy-ai--copied': copied }"
                                @click="copyForAi"
                                aria-label="Copy analysis formatted for AI assistant"
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
                            <span class="loading-title">ANALYZING SIGNAL</span>
                            <span class="loading-sub">Isolating root cause from stack trace…</span>
                        </div>

                        <!-- Empty State -->
                        <div v-else-if="!result" class="al-empty-state">
                            <div class="al-empty-state__icon" aria-hidden="true">
                                <svg width="22" height="22" viewBox="0 0 20 20" fill="none">
                                    <circle cx="10" cy="10" r="8" stroke="currentColor" stroke-width="1.4"/>
                                    <path d="M10 6v5M10 14v.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
                                </svg>
                            </div>
                            <div class="al-empty-state__title">AWAITING ERROR SIGNAL</div>
                            <p class="al-empty-state__desc">
                                Paste an error or traceback on the left to extract problem, likely cause, fix, and verification.
                            </p>
                        </div>

                        <!-- Structured Results Hierarchy -->
                        <div v-else class="al-lens-artifact al-result" role="region" aria-label="Error analysis result">
                            <div class="al-result__section">
                                <span class="al-result__label">Problem</span>
                                <MarkdownRenderer :content="result.problem" class="al-result__value" />
                            </div>

                            <div class="al-result__section">
                                <span class="al-result__label">Likely Cause</span>
                                <MarkdownRenderer :content="result.cause" class="al-result__value" />
                            </div>

                            <div class="al-result__section">
                                <span class="al-result__label">Suggested Fix</span>
                                <MarkdownRenderer :content="result.fix" class="al-result__value" />
                            </div>

                            <div class="al-result__section">
                                <span class="al-result__label">Verification Checklist</span>
                                <ul class="al-result__list">
                                    <li v-for="(step, idx) in result.verification" :key="idx">
                                        <MarkdownRenderer :content="step" inline />
                                    </li>
                                </ul>
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

.label-optional {
    font-size: 0.7rem;
    color: var(--text-muted);
    font-weight: 400;
    text-transform: none;
    letter-spacing: normal;
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
