<script setup>
import { computed, ref } from 'vue';
import { VueFlow } from '@vue-flow/core';
import '@vue-flow/core/dist/style.css';

const props = defineProps({
    files: {
        type: Array,
        default: () => []
    },
    relationships: {
        type: Array,
        default: () => []
    },
    title: {
        type: String,
        default: 'Module Topology Map'
    }
});

const copied = ref(false);

const nodes = computed(() => {
    return props.files.map((file, index) => {
        // Compute filename basename and directory for clean display
        const parts = file.path.split('/');
        const basename = parts.pop() || file.path;
        const dir = parts.join('/');

        return {
            id: `file-${index}`,
            type: 'default',
            position: {
                x: (index % 3) * 260 + 40,
                y: Math.floor(index / 3) * 110 + 40
            },
            data: {
                label: basename,
                fullPath: file.path,
                dir: dir
            }
        };
    });
});

const edges = computed(() => {
    return props.relationships
        .map((rel, index) => {
            const sourceIndex = props.files.findIndex(f => f.path === rel.source);
            const targetIndex = props.files.findIndex(f => f.path === rel.target);

            if (sourceIndex === -1 || targetIndex === -1) {
                return null;
            }

            return {
                id: `edge-${index}`,
                source: `file-${sourceIndex}`,
                target: `file-${targetIndex}`,
                type: 'smoothstep',
                animated: true,
                style: { stroke: 'var(--accent)', strokeWidth: 1.5 }
            };
        })
        .filter(Boolean);
});

function getMapAiMarkdown() {
    const parts = [
        `# ArrowLens Codebase Module Relationships`,
        '',
        `Topology: ${props.title}`,
        '',
        `## Indexed Files (${props.files.length})`,
        ...props.files.map(f => `- \`${f.path}\``),
        ''
    ];

    if (props.relationships.length) {
        parts.push(
            `## Module Import Relationships (${props.relationships.length})`,
            ...props.relationships.map(rel => `- \`${rel.source}\` → \`${rel.target}\``)
        );
    } else {
        parts.push('## Module Import Relationships', '- None detected');
    }

    return parts.join('\n');
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
    <section class="imp-map" role="region" aria-label="Codebase module topology">
        <div class="imp-map__header">
            <div class="imp-map__title-group">
                <span class="imp-map__tag">TOPOLOGY</span>
                <h3 class="imp-map__title">{{ title }}</h3>
            </div>
            <div class="imp-map__actions">
                <div class="imp-map__stats">
                    <span>{{ files.length }} Files</span>
                    <span class="stat-dot">·</span>
                    <span>{{ edges.length }} Import Edges</span>
                </div>
                <button
                    type="button"
                    class="al-btn-copy-ai"
                    :class="{ 'al-btn-copy-ai--copied': copied }"
                    @click="copyMapForAi"
                    aria-label="Copy codebase relationships formatted for AI assistant"
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

        <div class="imp-map__canvas">
            <VueFlow
                :nodes="nodes"
                :edges="edges"
                fit-view-on-init
                :nodes-draggable="true"
                :nodes-connectable="false"
            />
        </div>
    </section>
</template>

<style scoped>
.imp-map {
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    overflow: hidden;
    background: var(--surface);
    box-shadow: var(--shadow-sm);
    width: 100%;
}

.imp-map__header {
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

.imp-map__title-group {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    flex-wrap: wrap;
    min-width: 0;
}

.imp-map__tag {
    font-family: var(--mono);
    font-size: 0.65rem;
    font-weight: 700;
    color: var(--accent);
    padding: 2px 6px;
    background: var(--accent-soft);
    border-radius: var(--radius-sm);
}

.imp-map__title {
    margin: 0;
    font-family: var(--heading);
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--text-h);
}

.imp-map__actions {
    display: flex;
    align-items: center;
    gap: var(--space-3);
    flex-wrap: wrap;
}

.imp-map__stats {
    font-family: var(--mono);
    font-size: 0.725rem;
    color: var(--text-muted);
    display: flex;
    align-items: center;
    gap: 6px;
}

.stat-dot {
    opacity: 0.5;
}

.imp-map__canvas {
    height: 420px;
    background: var(--bg);
    width: 100%;
    min-width: 0;
}

:deep(.vue-flow__node) {
    background: var(--surface);
    color: var(--text-h);
    border: 1px solid var(--border-strong);
    border-radius: var(--radius-sm);
    font-family: var(--mono);
    font-size: 0.75rem;
    font-weight: 600;
    padding: 6px 12px;
    box-shadow: var(--shadow-sm);
    max-width: 220px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    user-select: none;
}

:deep(.vue-flow__node:hover) {
    border-color: var(--accent);
    box-shadow: var(--shadow-md);
}

:deep(.vue-flow__edge-path) {
    stroke: var(--accent);
}
</style>