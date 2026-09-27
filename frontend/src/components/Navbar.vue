<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuth } from '../composables/useAuth';
import { useAccessibility } from '../composables/useAccessibility';
import logo from '../assets/logo.png';

const router = useRouter();
const route = useRoute();
const { logout, state: authState } = useAuth();
const {
    focusMode,
    toggleFocusMode,
    theme,
    toggleTheme,
    openPanel,
    spotlight,
    highContrast,
    reduceMotion
} = useAccessibility();

const mobileOpen = ref(false);

const activeModesCount = computed(() => {
    let count = 0;
    if (focusMode.value) count++;
    if (spotlight.value) count++;
    if (highContrast.value) count++;
    if (reduceMotion.value) count++;
    return count;
});

const userInitial = computed(() => {
    const name = authState.user?.username || 'U';
    return name.charAt(0).toUpperCase();
});

async function handleLogout() {
    await logout();
    router.push('/');
}

function closeMobile() {
    mobileOpen.value = false;
}

function handleEscape(e) {
    if (e.key === 'Escape' && mobileOpen.value) {
        closeMobile();
    }
}

onMounted(() => {
    window.addEventListener('keydown', handleEscape);
});

onUnmounted(() => {
    window.removeEventListener('keydown', handleEscape);
});

function navigateToSection(hash) {
    closeMobile();
    if (route.path === '/dashboard') {
        const el = document.querySelector(hash);
        if (el) {
            el.scrollIntoView({ behavior: 'smooth' });
        }
    } else {
        router.push(`/dashboard${hash}`);
    }
}
</script>

<template>
    <!-- Focus Mode Floating Exit Dock -->
    <Transition name="focus-dock">
        <div v-if="focusMode" class="al-focus-dock" role="status">
            <span class="al-focus-dot-pulse" aria-hidden="true"></span>
            <span class="al-focus-label">FOCUS ACTIVE</span>
            <button
                type="button"
                class="al-btn al-btn--secondary al-btn--sm"
                @click="toggleFocusMode"
                aria-label="Exit focus mode"
            >
                Exit Focus
            </button>
        </div>
    </Transition>

    <!-- Mobile Top Navigation Header -->
    <header class="al-mobile-header">
        <button
            type="button"
            class="al-mobile-toggle"
            aria-label="Toggle navigation menu"
            :aria-expanded="mobileOpen"
            @click="mobileOpen = !mobileOpen"
        >
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true">
                <path d="M3 5h14M3 10h14M3 15h14" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
            </svg>
        </button>

        <router-link
            to="/dashboard"
            class="al-brand-lockup al-brand-lockup--mobile"
            aria-label="ArrowLens dashboard"
            @click="closeMobile"
        >
            <img :src="logo" alt="" aria-hidden="true" class="al-brand-lockup__mark" />
            <span class="al-brand-lockup__wordmark">ArrowLens</span>
        </router-link>

        <div class="al-mobile-actions">
            <button
                type="button"
                class="al-pill-btn"
                :class="{ 'al-pill-btn--active': focusMode }"
                :aria-pressed="focusMode"
                @click="toggleFocusMode"
                title="Toggle focus mode"
            >
                {{ focusMode ? 'Focused' : 'Focus' }}
            </button>
        </div>
    </header>

    <!-- Mobile Drawer Backdrop -->
    <div
        v-if="mobileOpen"
        class="al-sidebar-backdrop"
        @click="closeMobile"
        aria-hidden="true"
    ></div>

    <!-- Application Shell Left Sidebar -->
    <aside
        class="al-sidebar"
        :class="{ 'al-sidebar--mobile-open': mobileOpen, 'al-sidebar--focus': focusMode }"
        aria-label="Application sidebar"
    >
        <!-- Top Brand Section -->
        <div class="al-sidebar__brand-row">
            <router-link
                to="/dashboard"
                class="al-brand-lockup al-brand-lockup--sidebar"
                aria-label="ArrowLens dashboard"
                @click="closeMobile"
            >
                <img :src="logo" alt="" aria-hidden="true" class="al-brand-lockup__mark" />
                <span class="al-brand-lockup__wordmark">ArrowLens</span>

            </router-link>

            <button
                type="button"
                class="al-sidebar__focus-btn"
                :class="{ 'al-sidebar__focus-btn--active': focusMode }"
                :aria-pressed="focusMode"
                @click="toggleFocusMode"
                title="Toggle focus mode"
            >
                <span class="al-focus-dot"></span>
                <span>{{ focusMode ? 'Exit focus' : 'Focus' }}</span>
            </button>
        </div>

        <nav class="al-sidebar__nav">

            <!-- ── WORKSPACE GROUP ─────────────────────────────── -->
            <div class="al-nav-group">
                <span class="al-nav-group__label">WORKSPACE</span>
                <ul class="al-nav-list" role="list">
                    <li>
                        <router-link
                            to="/dashboard"
                            class="al-nav-item"
                            :class="{ 'is-active': route.path === '/dashboard' }"
                            @click="closeMobile"
                        >
                            <svg class="al-nav-icon" width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                                <rect x="2" y="2" width="5" height="5" rx="1" stroke="currentColor" stroke-width="1.3"/>
                                <rect x="9" y="2" width="5" height="5" rx="1" stroke="currentColor" stroke-width="1.3"/>
                                <rect x="2" y="9" width="5" height="5" rx="1" stroke="currentColor" stroke-width="1.3"/>
                                <rect x="9" y="9" width="5" height="5" rx="1" stroke="currentColor" stroke-width="1.3"/>
                            </svg>
                            <span class="al-nav-item__text">Dashboard</span>
                        </router-link>
                    </li>
                    <li>
                        <router-link
                            to="/error-lens"
                            class="al-nav-item"
                            :class="{ 'is-active': route.path === '/error-lens' }"
                            @click="closeMobile"
                        >
                            <span class="al-lens-num al-lens-num--error" aria-hidden="true">
                                <svg width="12" height="12" viewBox="0 0 16 16" fill="none">
                                    <path d="M8 2.2L14.2 13.5H1.8L8 2.2Z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/>
                                    <path d="M8 6.2v3.3M8 11.2v.3" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
                                </svg>
                            </span>
                            <span class="al-nav-item__text">Error Lens</span>
                        </router-link>
                    </li>
                    <li>
                        <router-link
                            to="/docs-lens"
                            class="al-nav-item"
                            :class="{ 'is-active': route.path === '/docs-lens' }"
                            @click="closeMobile"
                        >
                            <span class="al-lens-num al-lens-num--docs" aria-hidden="true">
                                <svg width="12" height="12" viewBox="0 0 16 16" fill="none">
                                    <path d="M3.5 2.5h6l3 3v8a1 1 0 0 1-1 1h-8a1 1 0 0 1-1-1v-10a1 1 0 0 1 1-1z" stroke="currentColor" stroke-width="1.3"/>
                                    <path d="M9.5 2.5v3h3M5.5 8h5M5.5 10.5h3.5" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
                                </svg>
                            </span>
                            <span class="al-nav-item__text">Docs Lens</span>
                        </router-link>
                    </li>
                    <li>
                        <router-link
                            to="/plan-lens"
                            class="al-nav-item"
                            :class="{ 'is-active': route.path === '/plan-lens' }"
                            @click="closeMobile"
                        >
                            <span class="al-lens-num al-lens-num--plan" aria-hidden="true">
                                <svg width="12" height="12" viewBox="0 0 16 16" fill="none">
                                    <circle cx="3.5" cy="4" r="1.5" stroke="currentColor" stroke-width="1.3"/>
                                    <circle cx="12.5" cy="12" r="1.5" stroke="currentColor" stroke-width="1.3"/>
                                    <path d="M5 4h3.5a2.5 2.5 0 0 1 2.5 2.5v3a2.5 2.5 0 0 0 2.5 2.5H11" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
                                </svg>
                            </span>
                            <span class="al-nav-item__text">Plan Lens</span>
                        </router-link>
                    </li>
                    <li>
                        <router-link
                            to="/codebase-lens"
                            class="al-nav-item"
                            :class="{ 'is-active': route.path === '/codebase-lens' }"
                            @click="closeMobile"
                        >
                            <span class="al-lens-num al-lens-num--codebase" aria-hidden="true">
                                <svg width="12" height="12" viewBox="0 0 16 16" fill="none">
                                    <rect x="2" y="2.5" width="5" height="4" rx="1" stroke="currentColor" stroke-width="1.3"/>
                                    <rect x="9" y="2.5" width="5" height="4" rx="1" stroke="currentColor" stroke-width="1.3"/>
                                    <rect x="5.5" y="9.5" width="5" height="4" rx="1" stroke="currentColor" stroke-width="1.3"/>
                                    <path d="M4.5 6.5v1.5a1 1 0 0 0 1 1h5a1 1 0 0 0 1-1V6.5" stroke="currentColor" stroke-width="1.2"/>
                                </svg>
                            </span>
                            <span class="al-nav-item__text">Codebase Lens</span>
                        </router-link>
                    </li>
                </ul>
            </div>

            <!-- ── HISTORY GROUP ──────────────────────────────── -->
            <div class="al-nav-group">
                <span class="al-nav-group__label">HISTORY & NOTES</span>
                <ul class="al-nav-list" role="list">
                    <li>
                        <a
                            href="#recent-activity"
                            class="al-nav-item"
                            @click.prevent="navigateToSection('#recent-activity')"
                        >
                            <svg class="al-nav-icon" width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                                <circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="1.3"/>
                                <path d="M8 5v3.5l2.5 1.5" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
                            </svg>
                            <span class="al-nav-item__text">Recent Activity</span>
                        </a>
                    </li>
                    <li>
                        <a
                            href="#notes"
                            class="al-nav-item"
                            @click.prevent="navigateToSection('#notes')"
                        >
                            <svg class="al-nav-icon" width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                                <path d="M3 2.5h10a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1v-9a1 1 0 0 1 1-1z" stroke="currentColor" stroke-width="1.3"/>
                                <path d="M5 6h6M5 9h4" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
                            </svg>
                            <span class="al-nav-item__text">Notes</span>
                        </a>
                    </li>
                </ul>
            </div>

            <!-- ── CALIBRATION GROUP ──────────────────────────── -->
            <div class="al-nav-group">
                <span class="al-nav-group__label">CALIBRATION</span>
                <ul class="al-nav-list" role="list">
                    <li>
                        <button
                            type="button"
                            class="al-nav-item al-nav-item--btn"
                            @click="openPanel"
                        >
                            <svg class="al-nav-icon" width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                                <circle cx="8" cy="8" r="7" stroke="currentColor" stroke-width="1.3"/>
                                <path d="M5 8h6M8 8v5M8 3v2" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
                            </svg>
                            <span class="al-nav-item__text">Accessibility</span>
                            <span v-if="activeModesCount > 0" class="al-a11y-pill">
                                {{ activeModesCount }} ON
                            </span>
                        </button>
                    </li>
                </ul>
            </div>

        </nav>

        <!-- ── ACCOUNT & LOGOUT (Bottom) ────────────────────── -->
        <div class="al-sidebar__footer">
            <button
                type="button"
                class="al-theme-toggle"
                :aria-label="`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`"
                @click="toggleTheme"
            >
                <svg v-if="theme === 'dark'" width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                    <circle cx="8" cy="8" r="3" stroke="currentColor" stroke-width="1.3"/>
                    <path d="M8 1.5v1.25M8 13.25v1.25M14.5 8h-1.25M2.75 8H1.5m11.1-4.6-.88.88m-7.44 7.44-.88.88m9.2 0-.88-.88M4.4 4.4l-.88-.88" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
                </svg>
                <svg v-else width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                    <path d="M13.7 9.4A6 6 0 0 1 6.6 2.3 6 6 0 1 0 13.7 9.4Z" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/>
                </svg>
                <span>{{ theme === 'dark' ? 'Light mode' : 'Dark mode' }}</span>
            </button>

            <div class="al-user-card" v-if="authState.user">
                <div class="al-user-avatar" aria-hidden="true">
                    {{ userInitial }}
                </div>
                <div class="al-user-info">
                    <span class="al-user-name">{{ authState.user.username }}</span>
                    <span class="al-user-status">Verified Workspace</span>
                </div>
            </div>

            <button
                type="button"
                class="al-logout-btn"
                :disabled="authState.loading"
                @click="handleLogout"
            >
                <svg width="15" height="15" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                    <path d="M6 2H3a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h3M10 11.5l3.5-3.5L10 4.5M13.5 8H5" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span>{{ authState.loading ? 'Signing out…' : 'Sign out' }}</span>
            </button>
        </div>

    </aside>
</template>

<style scoped>
/* ── Mobile Top Header ────────────────────────────────────────── */
.al-mobile-header {
    display: none;
    position: sticky;
    top: 0;
    z-index: 80;
    height: 54px;
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 0 var(--space-4);
    align-items: center;
    justify-content: space-between;
}

.al-mobile-toggle {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    background: transparent;
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    color: var(--text-h);
    cursor: pointer;
}

.al-pill-btn {
    font-family: var(--mono);
    font-size: 0.725rem;
    font-weight: 600;
    padding: 4px 10px;
    background: var(--surface-alt);
    border: 1px solid var(--border);
    border-radius: 14px;
    color: var(--text-muted);
    cursor: pointer;
}

.al-pill-btn--active {
    background: var(--accent);
    color: var(--accent-text);
    border-color: var(--accent);
}

/* ── Mobile Backdrop ──────────────────────────────────────────── */
.al-sidebar-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.45);
    z-index: 140;
    backdrop-filter: blur(3px);
}

/* ── Application Shell Left Sidebar ───────────────────────────── */
.al-sidebar {
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    width: var(--sidebar-w);
    background: var(--surface);
    border-right: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    z-index: 150;
    user-select: none;
    transition: transform 0.25s var(--ease-out);
}

.al-sidebar__brand-row {
    height: 64px;
    padding: 0 var(--space-5);
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid var(--border);
}

.al-sidebar__focus-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-family: var(--mono);
    font-size: 0.7rem;
    font-weight: 600;
    padding: 3px 8px;
    background: var(--surface-alt);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    color: var(--text-muted);
    cursor: pointer;
    transition: background 0.15s, border-color 0.15s, color 0.15s;
}

.al-sidebar__focus-btn:hover {
    color: var(--text-h);
    border-color: var(--border-strong);
}

.al-sidebar__focus-btn--active {
    background: var(--accent-soft);
    border-color: var(--accent);
    color: var(--accent);
}

.al-focus-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: currentColor;
}

/* ── Navigation Groups ────────────────────────────────────────── */
.al-sidebar__nav {
    flex: 1;
    overflow-y: auto;
    padding: var(--space-5) var(--space-3);
    display: flex;
    flex-direction: column;
    gap: var(--space-6);
}

.al-nav-group {
    display: flex;
    flex-direction: column;
    gap: var(--space-1);
}

.al-nav-group__label {
    font-family: var(--mono);
    font-size: 0.675rem;
    font-weight: 700;
    letter-spacing: 0.09em;
    color: var(--text-muted);
    padding: 0 var(--space-3);
    margin-bottom: var(--space-1);
}

.al-nav-list {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.al-nav-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 7px var(--space-3);
    border-radius: var(--radius-md);
    color: var(--text);
    text-decoration: none !important;
    font-size: 0.875rem;
    font-weight: 500;
    transition: background 0.15s, color 0.15s;
    position: relative;
}

.al-nav-item:hover {
    background: var(--surface-alt);
    color: var(--text-h);
}

.al-nav-item.is-active,
.al-nav-item.router-link-active {
    background: var(--surface-active);
    color: var(--text-h);
    font-weight: 600;
}

.al-nav-item.is-active::before,
.al-nav-item.router-link-active::before {
    content: "";
    position: absolute;
    left: 0;
    top: 6px;
    bottom: 6px;
    width: 3px;
    border-radius: 0 2px 2px 0;
    background: var(--accent);
}

.al-nav-item--btn {
    width: 100%;
    background: none;
    border: none;
    cursor: pointer;
    font-family: inherit;
    text-align: left;
}

.al-nav-icon {
    flex-shrink: 0;
    color: var(--text-muted);
}

.al-nav-item:hover .al-nav-icon,
.al-nav-item.is-active .al-nav-icon {
    color: var(--accent);
}

.al-lens-num {
    font-family: var(--mono);
    font-size: 0.725rem;
    font-weight: 700;
    width: 18px;
    height: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: var(--radius-sm);
    flex-shrink: 0;
}

.al-lens-num--error {
    background: var(--lens-error-bg);
    color: var(--lens-error);
    border: 1px solid var(--lens-error-border);
}

.al-lens-num--docs {
    background: var(--lens-docs-bg);
    color: var(--lens-docs);
    border: 1px solid var(--lens-docs-border);
}

.al-lens-num--plan {
    background: var(--lens-plan-bg);
    color: var(--lens-plan);
    border: 1px solid var(--lens-plan-border);
}

.al-lens-num--codebase {
    background: var(--lens-codebase-bg);
    color: var(--lens-codebase);
    border: 1px solid var(--lens-codebase-border);
}

.al-nav-item__text {
    flex: 1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.al-a11y-pill {
    font-family: var(--mono);
    font-size: 0.65rem;
    font-weight: 700;
    padding: 1px 5px;
    background: var(--accent);
    color: var(--accent-text);
    border-radius: 3px;
    margin-left: auto;
}

/* ── Sidebar Footer (Account & Logout) ────────────────────────── */
.al-sidebar__footer {
    padding: var(--space-4) var(--space-3);
    border-top: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
    background: var(--surface-alt);
}

.al-user-card {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 4px var(--space-2);
}

.al-user-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: var(--text-h);
    color: var(--bg);
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: var(--mono);
    font-weight: 700;
    font-size: 0.8rem;
    flex-shrink: 0;
}

.al-user-info {
    min-width: 0;
    display: flex;
    flex-direction: column;
}

.al-user-name {
    font-size: 0.825rem;
    font-weight: 600;
    color: var(--text-h);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.al-user-status {
    font-size: 0.7rem;
    color: var(--text-muted);
}

.al-logout-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    width: 100%;
    padding: 7px var(--space-3);
    border-radius: var(--radius-sm);
    background: transparent;
    border: 1px solid var(--border);
    color: var(--text-muted);
    font-family: var(--sans);
    font-size: 0.8rem;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.15s, color 0.15s, border-color 0.15s;
}

.al-logout-btn:hover {
    background: var(--error-bg);
    color: var(--error);
    border-color: var(--error);
}

.al-theme-toggle {
    display: flex;
    align-items: center;
    gap: 8px;
    width: 100%;
    padding: 8px var(--space-3);
    border: 1px solid transparent;
    border-radius: var(--radius-sm);
    background: transparent;
    color: var(--text);
    font-family: var(--sans);
    font-size: 0.8rem;
    font-weight: 550;
    text-align: left;
    cursor: pointer;
    transition: background var(--duration-fast), border-color var(--duration-fast), color var(--duration-fast);
}

.al-theme-toggle:hover {
    background: var(--surface);
    border-color: var(--border);
    color: var(--text-h);
}

.al-focus-dock {
    position: fixed;
    top: 12px;
    right: 16px;
    z-index: 200;
    display: flex;
    align-items: center;
    gap: var(--space-2);
    padding: 6px 8px 6px 12px;
    border: 1px solid var(--border-strong);
    border-radius: var(--radius-md);
    background: var(--surface);
    color: var(--text);
    box-shadow: var(--shadow-sm);
}

.al-focus-dot-pulse {
    width: 8px;
    height: 8px;
    flex: 0 0 auto;
    border-radius: 50%;
    background: var(--success);
}

.al-focus-label {
    color: var(--text-muted);
    font-family: var(--mono);
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    white-space: nowrap;
}

/* ── Responsive Adaptations ──────────────────────────────────── */
@media (max-width: 767px) {
    .al-mobile-header {
        display: flex;
    }

    .al-sidebar {
        transform: translateX(-100%);
        width: 280px;
        box-shadow: 10px 0 30px rgba(0, 0, 0, 0.2);
    }

    .al-sidebar--mobile-open {
        transform: translateX(0);
    }

    .al-focus-dock {
        top: 62px;
        right: 12px;
    }
}
</style>
