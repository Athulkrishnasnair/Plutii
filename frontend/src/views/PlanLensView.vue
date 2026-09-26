<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { analyzePlan } from '../services/api';
import Navbar from '../components/Navbar.vue';
import PlanImplementationMap from '../components/PlanImplementationMap.vue';

const route = useRoute();
const content = ref('');

const result = ref(null);
const loading = ref(false);
const apiError = ref('');
const copied = ref(false);

onMounted(() => {
    if (route.query.note) {
        content.value = route.query.note;
    }
});

function loadSample() {
    content.value = `Implement a distributed rate limiting middleware for public API endpoints.
Use Redis token bucket algorithm with sliding window counters.
Return HTTP 429 Too Many Requests with Retry-After and X-RateLimit headers.
Add Prometheus metrics tracking request volume per client API key.`;
}

function clearAll() {
    content.value = '';
    result.value = null;
    apiError.value = '';
}

async function handleAnalyze() {
    if (!content.value.trim()) return;
    loading.value = true;
    apiError.value = '';
    result.value = null;

    try {
        result.value = await analyzePlan(content.value.trim());
    } catch (err) {
        apiError.value =
            err.message ||
            'ArrowLens could not generate an implementation plan. Please check your connection and try again.';
    } finally {
        loading.value = false;
    }
}

function copyPlan() {
    if (!result.value) return;
    const text = [
        `PLAN: ${result.value.title}`,
        `GOAL: ${result.value.goal}`,
        `\nSTEPS:`,
        ...(result.value.steps || []).map((s, i) =>
            `\n${i + 1}. ${s.title}\n` +
            (s.actions || []).map(a => `   - ${a}`).join('\n') +
            (s.dependencies?.length ? `\n   Dependencies: ${s.dependencies.join(', ')}` : '')
        ),
        `\nVERIFICATION:`,
        ...(result.value.verification || []).map(v => `- ${v}`)
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
                    <span class="al-page-eyebrow">03 / PLAN LENS</span>
                    <h1 class="al-page-title">Architecture & Implementation Planner</h1>
                    <p class="al-page-desc">
                        Provide a feature concept or engineering note. ArrowLens structures it into
                        a sequenced implementation roadmap, dependency milestones, and verification tests.
                    </p>
                </header>

                <div class="al-workspace al-workspace--natural">

                    <!-- Left: Input Workspace Panel -->
                    <section class="al-workspace__panel" aria-labelledby="plan-input-heading">
                        <div class="al-workspace__panel-header">
                            <span id="plan-input-heading">DEVELOPER NOTE SPECIFICATION</span>
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
                            <form @submit.prevent="handleAnalyze" novalidate>
                                <div class="al-form-group">
                                    <label for="pl-note" class="al-label">
                                        <span>What are you building or refactoring?</span>
                                        <span class="field-required">*</span>
                                    </label>
                                    <textarea
                                        id="pl-note"
                                        v-model="content"
                                        class="al-textarea"
                                        placeholder="Describe the feature, architecture change, or technical task you want to sequence…"
                                        rows="13"
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
                                    <span v-if="loading" class="al-spinner" role="status" aria-label="Building plan…"></span>
                                    <span v-else>Generate Implementation Plan</span>
                                    <svg v-if="!loading" aria-hidden="true" class="al-btn__arrow" width="16" height="16" viewBox="0 0 16 16" fill="none">
                                        <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                                    </svg>
                                </button>
                            </form>
                        </div>
                    </section>

                    <!-- Right: Implementation Plan Artifact Panel -->
                    <section class="al-workspace__panel" aria-labelledby="plan-result-heading">
                        <div class="al-workspace__panel-header">
                            <span id="plan-result-heading">IMPLEMENTATION ARTIFACT</span>
                            <button
                                v-if="result"
                                type="button"
                                class="text-link-btn"
                                @click="copyPlan"
                            >
                                {{ copied ? 'Copied ✓' : 'Copy Plan' }}
                            </button>
                        </div>

                        <!-- Loading State -->
                        <div v-if="loading" class="al-loading-state" role="status" aria-live="polite">
                            <div class="al-spinner"></div>
                            <span class="loading-title">GENERATING ROADMAP</span>
                            <span class="loading-sub">Sequencing milestones and constructing dependency graph…</span>
                        </div>

                        <!-- Empty State -->
                        <div v-else-if="!result" class="al-empty-state">
                            <div class="al-empty-state__icon" aria-hidden="true">
                                <svg width="22" height="22" viewBox="0 0 20 20" fill="none">
                                    <path d="M3 4h14M3 8h10M3 12h14M3 16h8" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
                                </svg>
                            </div>
                            <div class="al-empty-state__title">AWAITING DEVELOPER SPECIFICATION</div>
                            <p class="al-empty-state__desc">
                                Provide an idea or engineering note on the left to generate an actionable implementation roadmap.
                            </p>
                        </div>

                        <!-- Structured Engineering Plan Artifact -->
                        <div v-else class="al-result" role="region" aria-label="Implementation plan">
                            <!-- Plan Title -->
                            <div class="al-result__section plan-header-section">
                                <span class="al-result__label">PLAN TITLE</span>
                                <h2 class="plan-artifact-title">{{ result.title }}</h2>
                            </div>

                            <!-- Goal -->
                            <div class="al-result__section">
                                <span class="al-result__label">ENGINEERING GOAL</span>
                                <p class="al-result__value">{{ result.goal }}</p>
                            </div>

                            <!-- Steps Breakdown -->
                            <div class="al-result__section">
                                <span class="al-result__label">IMPLEMENTATION MILESTONES</span>

                                <div class="plan-step-list">
                                    <article
                                        v-for="(step, idx) in result.steps"
                                        :key="idx"
                                        class="plan-step-item"
                                    >
                                        <div class="plan-step-item__marker" aria-hidden="true">
                                            {{ String(idx + 1).padStart(2, '0') }}
                                        </div>

                                        <div class="plan-step-item__content">
                                            <h3 class="plan-step-item__title">
                                                {{ step.title }}
                                            </h3>

                                            <ul class="al-result__list plan-action-list">
                                                <li v-for="action in step.actions" :key="action">
                                                    {{ action }}
                                                </li>
                                            </ul>

                                            <div v-if="step.dependencies?.length" class="plan-step-dep-row">
                                                <span class="dep-label">DEPENDENCIES:</span>
                                                <span
                                                    v-for="dep in step.dependencies"
                                                    :key="dep"
                                                    class="dep-pill"
                                                >
                                                    {{ dep }}
                                                </span>
                                            </div>
                                        </div>
                                    </article>
                                </div>
                            </div>

                            <!-- Verification -->
                            <div class="al-result__section">
                                <span class="al-result__label">VERIFICATION CHECKLIST</span>
                                <ul class="al-result__list">
                                    <li v-for="v in result.verification" :key="v">
                                        {{ v }}
                                    </li>
                                </ul>
                            </div>

                        </div>
                    </section>

                </div>

                <PlanImplementationMap
                    v-if="result?.steps?.length"
                    :steps="result.steps"
                />

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

.plan-header-section {
    background: var(--surface-alt);
    border-bottom: 1px solid var(--border);
}

.plan-artifact-title {
    font-family: var(--heading);
    font-size: 1.25rem;
    font-weight: 650;
    color: var(--text-h);
    margin: 0;
    letter-spacing: -0.02em;
}

.plan-step-list {
    display: flex;
    flex-direction: column;
    gap: var(--space-4);
    margin-top: var(--space-3);
}

.plan-step-item {
    display: flex;
    gap: var(--space-4);
    padding: var(--space-4) 0;
    border-top: 1px solid var(--border);
    min-width: 0;
}

.plan-step-item:first-child {
    border-top: none;
    padding-top: 0;
}

.plan-step-item__marker {
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

.plan-step-item__content {
    flex: 1;
    min-width: 0;
    overflow-wrap: anywhere;
}

.plan-step-item__title {
    font-family: var(--heading);
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--text-h);
    margin: 0 0 var(--space-2);
}

.plan-action-list {
    font-size: 0.885rem;
}

.plan-step-dep-row {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    flex-wrap: wrap;
    margin-top: var(--space-3);
    padding-top: var(--space-2);
    border-top: 1px dashed var(--border);
}

.dep-label {
    font-family: var(--mono);
    font-size: 0.65rem;
    font-weight: 700;
    color: var(--text-muted);
}

.dep-pill {
    font-family: var(--mono);
    font-size: 0.7rem;
    padding: 2px 6px;
    background: var(--surface-alt);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    color: var(--text-h);
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