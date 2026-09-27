<script setup>
import { computed, ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { getAnalysisHistory } from '../services/api';
import Navbar from '../components/Navbar.vue';
import MarkdownRenderer from '../components/MarkdownRenderer.vue';
import CodeBlock from '../components/CodeBlock.vue';

const route = useRoute();
const router = useRouter();

const analysis = ref(null);
const loading = ref(true);
const error = ref('');
const copied = ref(false);

const lensType = computed(() => analysis.value?.lens_type || '');

const lensTitle = computed(() => {
    const titles = {
        error: 'Error Lens Analysis',
        docs: 'Docs Lens Distillation',
        plan: 'Plan Lens Roadmap'
    };
    return titles[lensType.value] || 'Analysis Artifact';
});

async function loadAnalysis() {
    try {
        const history = await getAnalysisHistory();
        const id = Number(route.params.id);
        analysis.value = history.find(item => item.id === id) || null;

        if (!analysis.value) {
            error.value = 'Requested analysis artifact was not found.';
        }
    } catch (err) {
        error.value = err.message || 'Could not load this analysis.';
    } finally {
        loading.value = false;
    }
}

function goBack() {
    router.push('/dashboard');
}

function getAiMarkdown() {
    if (!analysis.value?.result) return '';
    const res = analysis.value.result;
    const type = lensType.value;

    if (type === 'error') {
        return [
            '# ArrowLens Error Analysis',
            '',
            '## Problem',
            res.problem || res.problem_statement || 'N/A',
            '',
            '## Likely Cause',
            res.likely_cause || res.cause || 'N/A',
            '',
            '## Suggested Fix',
            res.suggested_fix || res.fix || 'N/A',
            '',
            '## Verification',
            ...(res.verification || []).map(v => `- ${v}`)
        ].join('\n');
    }

    if (type === 'docs') {
        return [
            '# ArrowLens Documentation Analysis',
            '',
            '## Summary',
            res.summary || 'N/A',
            '',
            '## Key Concepts',
            ...(res.key_concepts || []).map(c => `- ${c}`),
            '',
            '## Example',
            '```',
            res.example || '',
            '```',
            '',
            '## Common Mistake',
            res.common_mistake || 'N/A'
        ].join('\n');
    }

    if (type === 'plan') {
        const parts = [
            '# ArrowLens Implementation Plan',
            '',
            '## Goal',
            res.goal || 'N/A',
            '',
            '## Steps'
        ];

        (res.steps || []).forEach((step, idx) => {
            parts.push('', `### ${idx + 1}. ${step.title}`, '', 'Actions:');
            (step.actions || []).forEach(a => parts.push(`- ${a}`));
            if (step.dependencies?.length) {
                parts.push('', `Dependencies: ${step.dependencies.join(', ')}`);
            }
        });

        if (res.verification?.length) {
            parts.push('', '## Verification', ...res.verification.map(v => `- ${v}`));
        }
        return parts.join('\n');
    }

    return JSON.stringify(res, null, 2);
}

async function copyForAi() {
    const text = getAiMarkdown();
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

onMounted(loadAnalysis);
</script>

<template>
    <div class="al-app-shell">
        <Navbar />

        <main class="al-app-main" id="main-content">
            <div class="al-container">

                <div class="history-nav-row">
                    <button
                        type="button"
                        class="al-btn al-btn--ghost al-btn--sm"
                        @click="goBack"
                    >
                        ← Return to Dashboard
                    </button>
                    <button
                        v-if="analysis"
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

                <div v-if="loading" class="al-loading-state" role="status">
                    <div class="al-spinner"></div>
                    <span>Retrieving analysis artifact…</span>
                </div>

                <div v-else-if="error" class="al-status-error" role="alert">
                    {{ error }}
                </div>

                <template v-else-if="analysis">
                    <!-- Header -->
                    <header class="al-page-header al-lens-header">
                        <div class="al-lens-eyebrow">
                            <span
                                class="al-lens-eyebrow__icon"
                                :class="`al-lens-eyebrow__icon--${lensType}`"
                                aria-hidden="true"
                            >
                                <svg v-if="lensType === 'error'" width="13" height="13" viewBox="0 0 16 16" fill="none">
                                    <path d="M8 2.2L14.2 13.5H1.8L8 2.2Z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/>
                                    <path d="M8 6.2v3.3M8 11.2v.3" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
                                </svg>
                                <svg v-else-if="lensType === 'docs'" width="13" height="13" viewBox="0 0 16 16" fill="none">
                                    <path d="M3.5 2.5h6l3 3v8a1 1 0 0 1-1 1h-8a1 1 0 0 1-1-1v-10a1 1 0 0 1 1-1z" stroke="currentColor" stroke-width="1.3"/>
                                    <path d="M9.5 2.5v3h3M5.5 8h5M5.5 10.5h3.5" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
                                </svg>
                                <svg v-else width="13" height="13" viewBox="0 0 16 16" fill="none">
                                    <circle cx="3.5" cy="4" r="1.5" stroke="currentColor" stroke-width="1.3"/>
                                    <circle cx="12.5" cy="12" r="1.5" stroke="currentColor" stroke-width="1.3"/>
                                    <path d="M5 4h3.5a2.5 2.5 0 0 1 2.5 2.5v3a2.5 2.5 0 0 0 2.5 2.5H11" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
                                </svg>
                            </span>
                            <span>{{ lensTitle }}</span>
                        </div>
                        <h1 class="al-page-title">{{ analysis.input }}</h1>
                        <p class="al-page-desc">
                            Recorded on {{ new Date(analysis.created_at).toLocaleString() }}
                        </p>
                    </header>

                    <!-- ERROR RESULT -->
                    <div v-if="lensType === 'error'" class="al-lens-artifact al-result history-result-card" role="region" aria-label="Error analysis">
                        <div class="al-result__section">
                            <span class="al-result__label">Problem</span>
                            <MarkdownRenderer :content="analysis.result.problem || analysis.result.problem_statement" class="al-result__value" />
                        </div>

                        <div class="al-result__section">
                            <span class="al-result__label">Likely Cause</span>
                            <MarkdownRenderer :content="analysis.result.likely_cause || analysis.result.cause" class="al-result__value" />
                        </div>

                        <div class="al-result__section">
                            <span class="al-result__label">Suggested Fix</span>
                            <MarkdownRenderer :content="analysis.result.suggested_fix || analysis.result.fix" class="al-result__value" />
                        </div>

                        <div class="al-result__section">
                            <span class="al-result__label">Verification Steps</span>
                            <ul class="al-result__list">
                                <li v-for="(item, idx) in analysis.result.verification" :key="idx">
                                    <MarkdownRenderer :content="item" inline />
                                </li>
                            </ul>
                        </div>
                    </div>

                    <!-- DOCS RESULT -->
                    <div v-else-if="lensType === 'docs'" class="al-lens-artifact al-result history-result-card" role="region" aria-label="Docs distillation">
                        <div class="al-result__section">
                            <span class="al-result__label">Summary</span>
                            <MarkdownRenderer :content="analysis.result.summary" class="al-result__value" />
                        </div>

                        <div class="al-result__section">
                            <span class="al-result__label">Key Concepts</span>
                            <ul class="al-result__list">
                                <li v-for="(concept, idx) in analysis.result.key_concepts" :key="idx">
                                    <MarkdownRenderer :content="concept" inline />
                                </li>
                            </ul>
                        </div>

                        <div class="al-result__section">
                            <span class="al-result__label">Working Example</span>
                            <CodeBlock :code="analysis.result.example" lang="python" />
                        </div>

                        <div class="al-result__section">
                            <span class="al-result__label">Common Mistake</span>
                            <MarkdownRenderer :content="analysis.result.common_mistake" class="al-result__value" />
                        </div>
                    </div>

                    <!-- PLAN RESULT -->
                    <div v-else-if="lensType === 'plan'" class="al-lens-artifact al-result history-result-card" role="region" aria-label="Implementation roadmap">
                        <div class="al-result__section">
                            <span class="al-result__label">Engineering Goal</span>
                            <MarkdownRenderer :content="analysis.result.goal" class="al-result__value" />
                        </div>

                        <div class="al-result__section">
                            <span class="al-result__label">Implementation Steps</span>
                            <div class="history-plan-steps">
                                <article
                                    v-for="(step, idx) in analysis.result.steps"
                                    :key="idx"
                                    class="history-step"
                                >
                                    <div class="history-step__num">
                                        {{ String(idx + 1).padStart(2, '0') }}
                                    </div>
                                    <div class="history-step__content">
                                        <h3>
                                            <MarkdownRenderer :content="step.title" inline />
                                        </h3>
                                        <ul class="al-result__list">
                                            <li v-for="(action, aIdx) in step.actions" :key="aIdx">
                                                <MarkdownRenderer :content="action" inline />
                                            </li>
                                        </ul>
                                        <div v-if="step.dependencies?.length" class="history-deps">
                                            <span>Dependencies: {{ step.dependencies.join(', ') }}</span>
                                        </div>
                                    </div>
                                </article>
                            </div>
                        </div>

                        <div class="al-result__section">
                            <span class="al-result__label">Verification</span>
                            <ul class="al-result__list">
                                <li v-for="(v, idx) in analysis.result.verification" :key="idx">
                                    <MarkdownRenderer :content="v" inline />
                                </li>
                            </ul>
                        </div>
                    </div>
                </template>

            </div>
        </main>
    </div>
</template>

<style scoped>
.history-nav-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: var(--space-3);
    margin-bottom: var(--space-6);
}

.history-result-card {
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    overflow: hidden;
    box-shadow: var(--shadow-sm);
    max-width: 880px;
    width: 100%;
    min-width: 0;
}

.history-code-block {
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

.history-plan-steps {
    display: flex;
    flex-direction: column;
    gap: var(--space-4);
    margin-top: var(--space-3);
}

.history-step {
    display: flex;
    gap: var(--space-4);
    padding: var(--space-3) 0;
    border-top: 1px solid var(--border);
}

.history-step:first-child {
    border-top: none;
    padding-top: 0;
}

.history-step__num {
    width: 28px;
    height: 28px;
    border-radius: var(--radius-sm);
    background: var(--surface-alt);
    border: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: var(--mono);
    font-size: 0.725rem;
    font-weight: 700;
    color: var(--accent);
    flex-shrink: 0;
}

.history-step__content h3 {
    font-family: var(--heading);
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--text-h);
    margin: 0 0 var(--space-2);
}

.history-step__content {
    min-width: 0;
    overflow-wrap: anywhere;
}

.history-deps {
    margin-top: var(--space-2);
    font-family: var(--mono);
    font-size: 0.725rem;
    color: var(--text-muted);
    overflow-wrap: anywhere;
}

@media (max-width: 640px) {
    .history-nav-row > * {
        max-width: 100%;
    }

    .history-result-card .al-result__section {
        padding-inline: var(--space-4);
    }

    .history-step {
        gap: var(--space-3);
    }
}
</style>