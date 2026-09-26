<script setup>
import { computed, ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { getAnalysisHistory } from '../services/api';
import Navbar from '../components/Navbar.vue';

const route = useRoute();
const router = useRouter();

const analysis = ref(null);
const loading = ref(true);
const error = ref('');
const copied = ref(false);

const lensType = computed(() => analysis.value?.lens_type || '');

const lensTitle = computed(() => {
    const titles = {
        error: '01 / Error Lens Analysis',
        docs: '02 / Docs Lens Distillation',
        plan: '03 / Plan Lens Roadmap'
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

function copyAnalysis() {
    if (!analysis.value) return;
    navigator.clipboard.writeText(JSON.stringify(analysis.value.result, null, 2));
    copied.value = true;
    setTimeout(() => {
        copied.value = false;
    }, 2000);
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
                        class="al-btn al-btn--secondary al-btn--sm"
                        @click="copyAnalysis"
                    >
                        {{ copied ? 'Copied JSON ✓' : 'Export JSON' }}
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
                    <header class="al-page-header">
                        <span class="al-page-eyebrow">{{ lensTitle }}</span>
                        <h1 class="al-page-title">{{ analysis.input }}</h1>
                        <p class="al-page-desc">
                            Recorded on {{ new Date(analysis.created_at).toLocaleString() }}
                        </p>
                    </header>

                    <!-- ERROR RESULT -->
                    <div v-if="lensType === 'error'" class="al-result history-result-card" role="region" aria-label="Error analysis">
                        <div class="al-result__section">
                            <span class="al-result__label">Problem</span>
                            <p class="al-result__value">{{ analysis.result.problem }}</p>
                        </div>

                        <div class="al-result__section">
                            <span class="al-result__label">Likely Cause</span>
                            <p class="al-result__value">{{ analysis.result.likely_cause }}</p>
                        </div>

                        <div class="al-result__section">
                            <span class="al-result__label">Suggested Fix</span>
                            <p class="al-result__value">{{ analysis.result.suggested_fix }}</p>
                        </div>

                        <div class="al-result__section">
                            <span class="al-result__label">Verification Steps</span>
                            <ul class="al-result__list">
                                <li v-for="(item, idx) in analysis.result.verification" :key="idx">
                                    {{ item }}
                                </li>
                            </ul>
                        </div>
                    </div>

                    <!-- DOCS RESULT -->
                    <div v-else-if="lensType === 'docs'" class="al-result history-result-card" role="region" aria-label="Docs distillation">
                        <div class="al-result__section">
                            <span class="al-result__label">Summary</span>
                            <p class="al-result__value">{{ analysis.result.summary }}</p>
                        </div>

                        <div class="al-result__section">
                            <span class="al-result__label">Key Concepts</span>
                            <ul class="al-result__list">
                                <li v-for="(concept, idx) in analysis.result.key_concepts" :key="idx">
                                    {{ concept }}
                                </li>
                            </ul>
                        </div>

                        <div class="al-result__section">
                            <span class="al-result__label">Working Example</span>
                            <pre class="history-code-block"><code>{{ analysis.result.example }}</code></pre>
                        </div>

                        <div class="al-result__section">
                            <span class="al-result__label">Common Mistake</span>
                            <p class="al-result__value">{{ analysis.result.common_mistake }}</p>
                        </div>
                    </div>

                    <!-- PLAN RESULT -->
                    <div v-else-if="lensType === 'plan'" class="al-result history-result-card" role="region" aria-label="Implementation roadmap">
                        <div class="al-result__section">
                            <span class="al-result__label">Engineering Goal</span>
                            <p class="al-result__value">{{ analysis.result.goal }}</p>
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
                                        <h3>{{ step.title }}</h3>
                                        <ul class="al-result__list">
                                            <li v-for="(action, aIdx) in step.actions" :key="aIdx">
                                                {{ action }}
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
                                    {{ v }}
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
    margin-bottom: var(--space-6);
}

.history-result-card {
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    overflow: hidden;
    box-shadow: var(--shadow-sm);
    max-width: 880px;
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

.history-deps {
    margin-top: var(--space-2);
    font-family: var(--mono);
    font-size: 0.725rem;
    color: var(--text-muted);
}
</style>