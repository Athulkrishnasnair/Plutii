<script setup>
import { computed, ref } from 'vue';
import { VueFlow } from '@vue-flow/core';
import '@vue-flow/core/dist/style.css';

const props = defineProps({
    steps: {
        type: Array,
        default: () => []
    },
    planTitle: {
        type: String,
        default: 'Implementation Plan'
    }
});

const copied = ref(false);

const nodes = computed(() => {
    return props.steps.map((step, index) => ({
        id: `step-${index}`,
        position: {
            x: 80,
            y: index * 100 + 40
        },
        data: {
            label: `${String(index + 1).padStart(2, '0')} // ${step.title}`
        },
        class: 'plan-flow-node'
    }));
});

const edges = computed(() => {
    return props.steps.slice(0, -1).map((_, index) => ({
        id: `edge-${index}`,
        source: `step-${index}`,
        target: `step-${index + 1}`,
        type: 'smoothstep',
        animated: true,
        style: { stroke: 'var(--accent)', strokeWidth: 2 }
    }));
});

function getMapAiMarkdown() {
    if (!props.steps || !props.steps.length) return '';
    const parts = [
        '# ArrowLens Implementation Map',
        '',
        `Plan: ${props.planTitle}`,
        `Total Milestones: ${props.steps.length}`,
        ''
    ];

    props.steps.forEach((step, idx) => {
        const nextStep = props.steps[idx + 1];
        parts.push(`${idx + 1}. ${step.title}`);
        if (step.actions?.length) {
            parts.push('   Actions:');
            step.actions.forEach(a => parts.push(`   - ${a}`));
        }
        if (step.dependencies?.length) {
            parts.push(`   Dependencies: ${step.dependencies.join(', ')}`);
        }
        if (nextStep) {
            parts.push(`   → Next: ${nextStep.title}`);
        }
        parts.push('');
    });

    return parts.join('\n').trim();
}

async function copyMapForAi() {
    const text = getMapAiMarkdown();
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
    <div class="plan-map" role="region" aria-label="Step-by-step dependency map">
        <div class="plan-map__header">
            <div class="plan-map__title-group">
                <span class="plan-map__tag">TOPOLOGY</span>
                <h3 class="plan-map__title">Implementation Map</h3>
            </div>
            <div class="plan-map__actions">
                <span class="plan-map__count">{{ steps.length }} Milestones</span>
                <button
                    type="button"
                    class="al-btn-copy-ai"
                    :class="{ 'al-btn-copy-ai--copied': copied }"
                    @click="copyMapForAi"
                    aria-label="Copy implementation map formatted for AI assistant"
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
        </div>

        <div class="plan-map__canvas">
            <VueFlow
                :nodes="nodes"
                :edges="edges"
                fit-view-on-init
                :nodes-draggable="false"
                :nodes-connectable="false"
            />
        </div>
    </div>
</template>

<style scoped>
.plan-map {
    margin-top: var(--space-8);
    min-width: 0;
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    overflow: hidden;
    background: var(--surface);
    box-shadow: var(--shadow-sm);
}

.plan-map__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--space-3) var(--space-5);
    background: var(--surface-alt);
    border-bottom: 1px solid var(--border);
    min-height: 48px;
    box-sizing: border-box;
    flex-wrap: wrap;
    gap: var(--space-3);
}

.plan-map__title-group {
    display: flex;
    align-items: center;
    gap: var(--space-2);
}

.plan-map__tag {
    font-family: var(--mono);
    font-size: 0.65rem;
    font-weight: 700;
    color: var(--accent);
    padding: 2px 6px;
    background: var(--accent-soft);
    border-radius: var(--radius-sm);
}

.plan-map__title {
    margin: 0;
    font-family: var(--heading);
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--text-h);
}

.plan-map__actions {
    display: flex;
    align-items: center;
    gap: var(--space-3);
}

.plan-map__count {
    font-family: var(--mono);
    font-size: 0.725rem;
    color: var(--text-muted);
}

.plan-map__canvas {
    height: 380px;
    width: 100%;
    min-width: 0;
    overflow: auto;
    overscroll-behavior: contain;
    background: var(--bg);
}

:deep(.vue-flow) {
    background: var(--surface-alt);
    color: var(--text);
}

@media (max-width: 640px) {
    .plan-map__canvas {
        height: 320px;
    }
}

:deep(.vue-flow__node) {
    background: var(--surface);
    color: var(--text-h);
    border: 1px solid var(--border-strong);
    border-radius: var(--radius-sm);
    font-family: var(--mono);
    font-size: 0.775rem;
    font-weight: 600;
    padding: 8px 14px;
    box-shadow: var(--shadow-sm);
    max-width: 320px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

:deep(.vue-flow__edge-path) {
    stroke: var(--accent);
}
</style>