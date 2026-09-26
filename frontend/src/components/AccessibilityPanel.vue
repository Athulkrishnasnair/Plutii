<script setup>
import { computed, onMounted, onUnmounted } from 'vue';
import { useAccessibility } from '../composables/useAccessibility';

const {
    textScale,
    focusMode,
    spotlight,
    highContrast,
    reduceMotion,
    toggleFocusMode,
    toggleSpotlight,
    toggleHighContrast,
    toggleReduceMotion,
    increaseText,
    decreaseText,
    resetText,
    resetAll,
    closePanel
} = useAccessibility();

const textPercent = computed(() => Math.round(textScale.value * 100));

// Close on Escape key
function handleKeyDown(e) {
    if (e.key === 'Escape') {
        closePanel();
    }
}

onMounted(() => {
    window.addEventListener('keydown', handleKeyDown);
});

onUnmounted(() => {
    window.removeEventListener('keydown', handleKeyDown);
});
</script>

<template>
    <aside
        class="a11y-panel"
        role="region"
        aria-label="Accessibility and display settings"
    >
        <header class="a11y-panel__header">
            <div>
                <span class="a11y-panel__eyebrow">INSTRUMENT CALIBRATION</span>
                <h2 class="a11y-panel__title">Accessibility</h2>
            </div>
            <button
                type="button"
                class="a11y-close-btn"
                aria-label="Close accessibility panel"
                @click="closePanel"
            >
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true">
                    <path d="M1.75 1.75l10.5 10.5M12.25 1.75L1.75 12.25" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
                </svg>
            </button>
        </header>

        <div class="a11y-panel__content">

            <!-- 01 TEXT SIZE -->
            <section class="a11y-section" aria-labelledby="a11y-text-heading">
                <div class="a11y-section__header">
                    <h3 id="a11y-text-heading" class="a11y-section__title">
                        01 / TEXT SIZE
                    </h3>
                    <button
                        v-if="textScale !== 1"
                        type="button"
                        class="a11y-reset-link"
                        @click="resetText"
                    >
                        Reset
                    </button>
                </div>

                <div class="a11y-scale-control">
                    <button
                        type="button"
                        class="a11y-scale-btn"
                        aria-label="Decrease font size"
                        :disabled="textScale <= 0.85"
                        @click="decreaseText"
                    >
                        A−
                    </button>

                    <div class="a11y-scale-readout" aria-live="polite">
                        <span class="a11y-scale-value">{{ textPercent }}%</span>
                        <span class="a11y-scale-sub">Reflow scale</span>
                    </div>

                    <button
                        type="button"
                        class="a11y-scale-btn"
                        aria-label="Increase font size"
                        :disabled="textScale >= 1.3"
                        @click="increaseText"
                    >
                        A+
                    </button>
                </div>
            </section>

            <!-- 02 FOCUS MODE -->
            <section class="a11y-section" aria-labelledby="a11y-focus-heading">
                <div class="a11y-toggle-card">
                    <div class="a11y-toggle-card__meta">
                        <div class="a11y-toggle-card__top">
                            <h3 id="a11y-focus-heading" class="a11y-section__title">
                                02 / FOCUS MODE
                            </h3>
                            <span
                                class="a11y-badge"
                                :class="focusMode ? 'a11y-badge--active' : 'a11y-badge--idle'"
                            >
                                {{ focusMode ? 'ON' : 'OFF' }}
                            </span>
                        </div>
                        <p class="a11y-toggle-desc">
                            Centers the active instrument, minimizes secondary sidebars, and suppresses decorative elements.
                        </p>
                    </div>

                    <button
                        type="button"
                        role="switch"
                        :aria-checked="focusMode"
                        class="a11y-switch"
                        :class="{ 'a11y-switch--on': focusMode }"
                        aria-label="Toggle focus mode"
                        @click="toggleFocusMode"
                    >
                        <span class="a11y-switch__knob"></span>
                    </button>
                </div>
            </section>

            <!-- 03 READING SPOTLIGHT -->
            <section class="a11y-section" aria-labelledby="a11y-spotlight-heading">
                <div class="a11y-toggle-card">
                    <div class="a11y-toggle-card__meta">
                        <div class="a11y-toggle-card__top">
                            <h3 id="a11y-spotlight-heading" class="a11y-section__title">
                                03 / READING SPOTLIGHT
                            </h3>
                            <span
                                class="a11y-badge"
                                :class="spotlight ? 'a11y-badge--active' : 'a11y-badge--idle'"
                            >
                                {{ spotlight ? 'ON' : 'OFF' }}
                            </span>
                        </div>
                        <p class="a11y-toggle-desc">
                            Illuminates the active or hovered card while gently dimming peripheral noise for high reading retention.
                        </p>
                    </div>

                    <button
                        type="button"
                        role="switch"
                        :aria-checked="spotlight"
                        class="a11y-switch"
                        :class="{ 'a11y-switch--on': spotlight }"
                        aria-label="Toggle reading spotlight"
                        @click="toggleSpotlight"
                    >
                        <span class="a11y-switch__knob"></span>
                    </button>
                </div>
            </section>

            <!-- 04 HIGH CONTRAST -->
            <section class="a11y-section" aria-labelledby="a11y-contrast-heading">
                <div class="a11y-toggle-card">
                    <div class="a11y-toggle-card__meta">
                        <div class="a11y-toggle-card__top">
                            <h3 id="a11y-contrast-heading" class="a11y-section__title">
                                04 / HIGH CONTRAST
                            </h3>
                            <span
                                class="a11y-badge"
                                :class="highContrast ? 'a11y-badge--active' : 'a11y-badge--idle'"
                            >
                                {{ highContrast ? 'ON' : 'OFF' }}
                            </span>
                        </div>
                        <p class="a11y-toggle-desc">
                            Enforces WCAG AAA contrast ratios, solid 2px hairline borders, and distinct focus rings.
                        </p>
                    </div>

                    <button
                        type="button"
                        role="switch"
                        :aria-checked="highContrast"
                        class="a11y-switch"
                        :class="{ 'a11y-switch--on': highContrast }"
                        aria-label="Toggle high contrast"
                        @click="toggleHighContrast"
                    >
                        <span class="a11y-switch__knob"></span>
                    </button>
                </div>
            </section>

            <!-- 05 REDUCE MOTION -->
            <section class="a11y-section" aria-labelledby="a11y-motion-heading">
                <div class="a11y-toggle-card">
                    <div class="a11y-toggle-card__meta">
                        <div class="a11y-toggle-card__top">
                            <h3 id="a11y-motion-heading" class="a11y-section__title">
                                05 / REDUCE MOTION
                            </h3>
                            <span
                                class="a11y-badge"
                                :class="reduceMotion ? 'a11y-badge--active' : 'a11y-badge--idle'"
                            >
                                {{ reduceMotion ? 'ON' : 'OFF' }}
                            </span>
                        </div>
                        <p class="a11y-toggle-desc">
                            Bypasses all decorative entrance animations, transitions, and kinetic canvas effects.
                        </p>
                    </div>

                    <button
                        type="button"
                        role="switch"
                        :aria-checked="reduceMotion"
                        class="a11y-switch"
                        :class="{ 'a11y-switch--on': reduceMotion }"
                        aria-label="Toggle reduce motion"
                        @click="toggleReduceMotion"
                    >
                        <span class="a11y-switch__knob"></span>
                    </button>
                </div>
            </section>

        </div>

        <footer class="a11y-panel__footer">
            <button
                type="button"
                class="al-btn al-btn--outline a11y-footer-reset"
                @click="resetAll"
            >
                Reset All Calibrations
            </button>
            <p class="a11y-footer-note">
                Preferences persist automatically across browser sessions.
            </p>
        </footer>
    </aside>
</template>

<style scoped>
.a11y-panel {
    display: flex;
    flex-direction: column;
    height: 100%;
    background: var(--surface);
    color: var(--text);
    overflow-y: auto;
}

.a11y-panel__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--space-6) var(--space-6) var(--space-4);
    border-bottom: 1px solid var(--border);
    position: sticky;
    top: 0;
    background: var(--surface);
    z-index: 10;
}

.a11y-panel__eyebrow {
    font-family: var(--mono);
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: var(--text-muted);
    display: block;
    margin-bottom: 3px;
}

.a11y-panel__title {
    font-family: var(--heading);
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-h);
    margin: 0;
}

.a11y-close-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    background: var(--surface-alt);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    color: var(--text-muted);
    cursor: pointer;
    transition: background 0.15s, color 0.15s, border-color 0.15s;
}

.a11y-close-btn:hover {
    background: var(--surface-active);
    color: var(--text-h);
    border-color: var(--border-strong);
}

.a11y-panel__content {
    flex: 1;
    padding: var(--space-6);
    display: flex;
    flex-direction: column;
    gap: var(--space-6);
}

.a11y-section {
    padding-bottom: var(--space-5);
    border-bottom: 1px solid var(--border);
}

.a11y-section:last-child {
    border-bottom: none;
    padding-bottom: 0;
}

.a11y-section__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: var(--space-3);
}

.a11y-section__title {
    font-family: var(--mono);
    font-size: 0.725rem;
    font-weight: 650;
    letter-spacing: 0.08em;
    color: var(--text-muted);
    margin: 0;
}

.a11y-reset-link {
    font-family: var(--mono);
    font-size: 0.7rem;
    color: var(--accent);
    background: none;
    border: none;
    cursor: pointer;
    text-decoration: underline;
    padding: 0;
}

/* Text Size Control */
.a11y-scale-control {
    display: flex;
    align-items: center;
    gap: var(--space-3);
    background: var(--surface-alt);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: var(--space-2);
}

.a11y-scale-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 44px;
    height: 40px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    color: var(--text-h);
    font-family: var(--mono);
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.15s, border-color 0.15s;
}

.a11y-scale-btn:hover:not(:disabled) {
    background: var(--surface-active);
    border-color: var(--border-strong);
}

.a11y-scale-btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
}

.a11y-scale-readout {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
}

.a11y-scale-value {
    font-family: var(--mono);
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text-h);
    line-height: 1.1;
}

.a11y-scale-sub {
    font-size: 0.7rem;
    color: var(--text-muted);
}

/* Toggle Card */
.a11y-toggle-card {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: var(--space-4);
}

.a11y-toggle-card__meta {
    flex: 1;
}

.a11y-toggle-card__top {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    margin-bottom: var(--space-1);
}

.a11y-badge {
    font-family: var(--mono);
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    padding: 1px 6px;
    border-radius: 3px;
}

.a11y-badge--active {
    background: var(--accent);
    color: var(--accent-text);
}

.a11y-badge--idle {
    background: var(--surface-alt);
    color: var(--text-muted);
    border: 1px solid var(--border);
}

.a11y-toggle-desc {
    font-size: 0.8rem;
    line-height: 1.45;
    color: var(--text-muted);
}

/* Accessible Switch Component */
.a11y-switch {
    width: 44px;
    height: 24px;
    background: var(--surface-alt);
    border: 1px solid var(--border-strong);
    border-radius: 12px;
    padding: 2px;
    cursor: pointer;
    flex-shrink: 0;
    position: relative;
    transition: background 0.2s ease, border-color 0.2s ease;
}

.a11y-switch__knob {
    display: block;
    width: 18px;
    height: 18px;
    background: var(--text-muted);
    border-radius: 50%;
    transition: transform 0.2s ease, background 0.2s ease;
}

.a11y-switch--on {
    background: var(--accent);
    border-color: var(--accent);
}

.a11y-switch--on .a11y-switch__knob {
    transform: translateX(20px);
    background: var(--surface);
}

/* Footer */
.a11y-panel__footer {
    padding: var(--space-5) var(--space-6);
    border-top: 1px solid var(--border);
    background: var(--surface-alt);
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
}

.a11y-footer-reset {
    width: 100%;
    justify-content: center;
    font-size: 0.8rem;
    padding: 8px 14px;
}

.a11y-footer-note {
    font-size: 0.725rem;
    color: var(--text-muted);
    text-align: center;
    line-height: 1.4;
}
</style>