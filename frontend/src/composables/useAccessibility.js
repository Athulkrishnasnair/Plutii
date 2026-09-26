import { ref, watch } from 'vue';

const storedTheme = localStorage.getItem('arrowlens-theme');
const systemPrefersDark = typeof window !== 'undefined' &&
    window.matchMedia &&
    window.matchMedia('(prefers-color-scheme: dark)').matches;
const theme = ref(
    storedTheme === 'light' || storedTheme === 'dark'
        ? storedTheme
        : systemPrefersDark ? 'dark' : 'light'
);

// Initialize text scale with bounds protection [0.85, 1.3]
const storedScale = Number(localStorage.getItem('arrowlens-text-scale'));
const textScale = ref(
    !isNaN(storedScale) && storedScale >= 0.85 && storedScale <= 1.3 ? storedScale : 1
);

const focusMode = ref(
    localStorage.getItem('arrowlens-focus') === 'true'
);

const spotlight = ref(
    localStorage.getItem('arrowlens-spotlight') === 'true'
);

const highContrast = ref(
    localStorage.getItem('arrowlens-high-contrast') === 'true'
);

// Check system prefers-reduced-motion as default if user hasn't explicitly set it
const systemPrefersReducedMotion = typeof window !== 'undefined' &&
    window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

const storedReduceMotion = localStorage.getItem('arrowlens-reduce-motion');
const reduceMotion = ref(
    storedReduceMotion !== null ? storedReduceMotion === 'true' : systemPrefersReducedMotion
);

// Accessibility panel visibility state
const isPanelOpen = ref(false);

function applyAccessibilitySettings() {
    if (typeof document === 'undefined') return;
    const root = document.documentElement;

    root.dataset.theme = theme.value;
    root.style.colorScheme = theme.value;

    root.style.setProperty(
        '--accessibility-text-scale',
        textScale.value
    );

    root.classList.toggle('focus-mode', focusMode.value);
    root.classList.toggle('spotlight-mode', spotlight.value);
    root.classList.toggle('high-contrast', highContrast.value);
    root.classList.toggle('reduce-motion', reduceMotion.value);
}

// Watchers
watch(theme, (value) => {
    localStorage.setItem('arrowlens-theme', value);
    applyAccessibilitySettings();
});

watch(textScale, (value) => {
    localStorage.setItem('arrowlens-text-scale', value);
    applyAccessibilitySettings();
});

watch(focusMode, (value) => {
    localStorage.setItem('arrowlens-focus', value);
    applyAccessibilitySettings();
});

watch(spotlight, (value) => {
    localStorage.setItem('arrowlens-spotlight', value);
    applyAccessibilitySettings();
});

watch(highContrast, (value) => {
    localStorage.setItem('arrowlens-high-contrast', value);
    applyAccessibilitySettings();
});

watch(reduceMotion, (value) => {
    localStorage.setItem('arrowlens-reduce-motion', value);
    applyAccessibilitySettings();
});

// Run immediately
applyAccessibilitySettings();

// Actions
function toggleFocusMode() {
    focusMode.value = !focusMode.value;
}

function toggleTheme() {
    theme.value = theme.value === 'dark' ? 'light' : 'dark';
}

function toggleSpotlight() {
    spotlight.value = !spotlight.value;
}

function toggleHighContrast() {
    highContrast.value = !highContrast.value;
}

function toggleReduceMotion() {
    reduceMotion.value = !reduceMotion.value;
}

function increaseText() {
    textScale.value = Math.min(1.3, Number((textScale.value + 0.05).toFixed(2)));
}

function decreaseText() {
    textScale.value = Math.max(0.85, Number((textScale.value - 0.05).toFixed(2)));
}

function resetText() {
    textScale.value = 1;
}

function resetAll() {
    textScale.value = 1;
    focusMode.value = false;
    spotlight.value = false;
    highContrast.value = false;
    reduceMotion.value = systemPrefersReducedMotion;
}

function openPanel() {
    isPanelOpen.value = true;
}

function closePanel() {
    isPanelOpen.value = false;
}

function togglePanel() {
    isPanelOpen.value = !isPanelOpen.value;
}

export function useAccessibility() {
    return {
        theme,
        textScale,
        focusMode,
        spotlight,
        highContrast,
        reduceMotion,
        isPanelOpen,
        toggleFocusMode,
        toggleTheme,
        toggleSpotlight,
        toggleHighContrast,
        toggleReduceMotion,
        increaseText,
        decreaseText,
        resetText,
        resetAll,
        openPanel,
        closePanel,
        togglePanel
    };
}