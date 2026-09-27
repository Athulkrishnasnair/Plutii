<script setup>
import { watch } from 'vue';
import { useRoute } from 'vue-router';
import { useAuth } from './composables/useAuth';
import { useAccessibility } from './composables/useAccessibility';
import AccessibilityPanel from './components/AccessibilityPanel.vue';

const { isPanelOpen, togglePanel, closePanel } = useAccessibility();
const route = useRoute();
const { resolveAuth } = useAuth();

// Boot initial auth resolution in parallel with router
resolveAuth();

// Manage landing vs dashboard body class
watch(
    () => route.path,
    (path) => {
        const appEl = document.getElementById('app');
        if (!appEl) return;
        appEl.classList.toggle('app--landing', path === '/');
    },
    { immediate: true }
);
</script>

<template>
    <a href="#main-content" class="al-skip-link">Skip to main content</a>

    <router-view />

    <!-- Accessible Floating Trigger -->
    <button
        class="a11y-trigger-btn"
        type="button"
        aria-label="Open accessibility calibrations"
        :aria-expanded="isPanelOpen"
        @click="togglePanel"
    >
        <svg width="15" height="15" viewBox="0 0 16 16" fill="none" aria-hidden="true">
            <circle cx="8" cy="8" r="7" stroke="currentColor" stroke-width="1.3"/>
            <circle cx="8" cy="4.5" r="1.25" fill="currentColor"/>
            <path d="M5 8h6M8 8v5M6 13h4" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
        </svg>
        <span>Accessibility</span>
    </button>

    <!-- Modal Drawer with Backdrop -->
    <Transition name="a11y-fade">
        <div
            v-if="isPanelOpen"
            class="a11y-backdrop"
            @click.self="closePanel"
            role="dialog"
            aria-modal="true"
            aria-label="Accessibility Settings"
        >
            <div class="a11y-sheet">
                <AccessibilityPanel />
            </div>
        </div>
    </Transition>
</template>

<style scoped>
/* Accessible Floating Launcher */
.a11y-trigger-btn {
    position: fixed;
    right: 20px;
    bottom: 20px;
    z-index: 900;

    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 14px;

    background: var(--surface);
    color: var(--text-h);
    border: 1px solid var(--border-strong);
    border-radius: var(--radius-md);

    font-family: var(--mono);
    font-size: 0.775rem;
    font-weight: 600;
    letter-spacing: 0.02em;

    box-shadow: var(--shadow-md);
    cursor: pointer;
    user-select: none;
    transition:
        background var(--duration-fast, 0.15s),
        border-color var(--duration-fast, 0.15s),
        transform var(--duration-fast, 0.15s),
        box-shadow var(--duration-fast, 0.15s);
}

.a11y-trigger-btn:hover {
    background: var(--surface-alt);
    border-color: var(--accent);
    transform: translateY(-1px);
    box-shadow: var(--shadow-lg);
}

.a11y-trigger-btn:active {
    transform: translateY(0);
}

/* Backdrop */
.a11y-backdrop {
    position: fixed;
    inset: 0;
    z-index: 1000;
    background: rgba(10, 12, 16, 0.45);
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
    display: flex;
    justify-content: flex-end;
}

/* Slide-out Sheet */
.a11y-sheet {
    width: min(380px, 92vw);
    height: 100%;
    background: var(--surface);
    border-left: 1px solid var(--border);
    box-shadow: -10px 0 35px rgba(0, 0, 0, 0.18);
    display: flex;
    flex-direction: column;
}

/* Transitions */
.a11y-fade-enter-active,
.a11y-fade-leave-active {
    transition: opacity 0.2s ease;
}

.a11y-fade-enter-from,
.a11y-fade-leave-to {
    opacity: 0;
}

.a11y-fade-enter-active .a11y-sheet,
.a11y-fade-leave-active .a11y-sheet {
    transition: transform 0.24s cubic-bezier(0.16, 1, 0.3, 1);
}

.a11y-fade-enter-from .a11y-sheet,
.a11y-fade-leave-to .a11y-sheet {
    transform: translateX(100%);
}
</style>