<script setup>
import { computed, ref } from 'vue';
import { ArrowRight, Menu, Moon, Sun, X } from '@lucide/vue';
import { useAuth } from '../composables/useAuth';
import { useAccessibility } from '../composables/useAccessibility';
import logo from '../assets/logo.png';

const { isAuthenticated } = useAuth();
const authed = computed(() => isAuthenticated());
const { theme, toggleTheme } = useAccessibility();
const mobileOpen = ref(false);
</script>

<template>
    <nav class="l-nav" aria-label="Site navigation">
        <div class="l-nav__inner">

            <!-- Logo mark + wordmark -->
            <a href="/" class="l-nav__brand al-brand-lockup al-brand-lockup--landing" aria-label="ArrowLens home">
                <img
                    :src="logo"
                    alt=""
                    aria-hidden="true"
                    class="al-brand-lockup__mark"
                />
                <span class="al-brand-lockup__wordmark">ArrowLens</span>
            </a>

            <!-- Primary nav links -->
            <ul id="landing-lens-navigation" class="l-nav__links" :class="{ 'l-nav__links--open': mobileOpen }" role="list">
                <li><router-link to="/error-lens" class="l-nav__link" @click="mobileOpen = false">Error Lens</router-link></li>
                <li><router-link to="/docs-lens" class="l-nav__link" @click="mobileOpen = false">Docs Lens</router-link></li>
                <li><router-link to="/plan-lens" class="l-nav__link" @click="mobileOpen = false">Plan Lens</router-link></li>
                <li><router-link to="/codebase-lens" class="l-nav__link" @click="mobileOpen = false">Codebase Lens</router-link></li>
            </ul>

            <button
                type="button"
                class="l-nav__menu-toggle"
                :aria-label="mobileOpen ? 'Close lens navigation' : 'Open lens navigation'"
                aria-controls="landing-lens-navigation"
                :aria-expanded="mobileOpen"
                @click="mobileOpen = !mobileOpen"
            >
                <X v-if="mobileOpen" :size="19" aria-hidden="true" />
                <Menu v-else :size="19" aria-hidden="true" />
            </button>

            <!-- Theme and auth actions -->
            <div class="l-nav__actions">
                <button
                    type="button"
                    class="l-nav__theme"
                    :aria-label="theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'"
                    :title="theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'"
                    @click="toggleTheme"
                >
                    <Sun v-if="theme === 'dark'" :size="17" :stroke-width="1.8" aria-hidden="true" />
                    <Moon v-else :size="17" :stroke-width="1.8" aria-hidden="true" />
                </button>
                <template v-if="authed">
                    <router-link to="/dashboard" class="l-nav__cta">
                        Dashboard
                        <ArrowRight :size="15" :stroke-width="1.7" aria-hidden="true" />
                    </router-link>
                </template>
                <template v-else>
                    <router-link to="/login" class="l-nav__signin">Sign in</router-link>
                    <router-link to="/register" class="l-nav__cta">
                        Get started
                        <ArrowRight :size="15" :stroke-width="1.7" aria-hidden="true" />
                    </router-link>
                </template>
            </div>

        </div>
    </nav>
</template>

<style scoped>
.l-nav {
    position: sticky;
    top: 0;
    z-index: 100;
    background: color-mix(in srgb, var(--bg) 94%, transparent);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--border);
}

.l-nav__inner {
    max-width: var(--l-max);
    margin: 0 auto;
    padding: 0 24px;
    height: 56px;
    display: flex;
    align-items: center;
    gap: 16px;
}

.l-nav__brand {
    flex-shrink: 0;
}

.l-nav__links {
    display: flex;
    align-items: center;
    gap: 2px;
    list-style: none;
    margin: 0;
    padding: 0;
    flex: 1;
    min-width: 0;
}

.l-nav__link {
    font-size: calc((14px) * var(--accessibility-text-scale, 1));
    color: var(--text);
    text-decoration: none;
    padding: 6px 8px;
    border-radius: var(--radius-sm);
    white-space: nowrap;
    transition: color var(--duration-fast), background var(--duration-fast);
}

.l-nav__link:hover {
    color: var(--text-h);
    background: var(--l-surface);
    text-decoration: none;
}

.l-nav__link:focus-visible,
.l-nav__signin:focus-visible,
.l-nav__cta:focus-visible {
    outline: 2px solid var(--border-focus);
    outline-offset: 2px;
}

.l-nav__signin:hover {
    color: var(--text-h);
    text-decoration: underline;
    text-underline-offset: 3px;
}

.l-nav__actions {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 10px;
    flex-shrink: 0;
}

.l-nav__menu-toggle {
    display: none;
}

.l-nav__signin {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-height: 36px;
    padding: 7px 8px;
    color: var(--text);
    font-size: calc((14px) * var(--accessibility-text-scale, 1));
    font-weight: 500;
    text-decoration: none;
    border-radius: var(--radius-sm);
    transition: color var(--duration-fast), background var(--duration-fast);
}

.l-nav__signin:hover {
    background: var(--surface-alt);
    text-decoration: none;
}

.l-nav__theme {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    padding: 0;
    color: var(--text-muted);
    background: transparent;
    border: 1px solid transparent;
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: color var(--duration-fast), background var(--duration-fast), border-color var(--duration-fast);
}

.l-nav__theme:hover {
    color: var(--text-h);
    background: var(--surface-alt);
    border-color: var(--border);
}

.l-nav__theme:focus-visible {
    outline: 2px solid var(--border-focus);
    outline-offset: 2px;
}

.l-nav__cta {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: calc((14px) * var(--accessibility-text-scale, 1));
    font-weight: 500;
    color: var(--bg);
    background: var(--text-h);
    text-decoration: none;
    min-height: 36px;
    padding: 7px 12px;
    border: 1px solid var(--text-h);
    border-radius: var(--radius-md);
    transition: background var(--duration-fast), border-color var(--duration-fast), gap var(--duration-fast);
}

.l-nav__cta:hover {
    background: var(--accent-hover);
    gap: 9px;
}

.l-nav__cta:focus-visible {
    outline: 2px solid var(--accent);
    outline-offset: 3px;
}

:root[data-theme="dark"] .l-nav__cta {
    background: var(--text-h);
    color: var(--bg);
}

:root[data-theme="dark"] .l-nav__cta:hover {
    background: #e8e8f0;
}

@media (max-width: 640px) {
    .l-nav__inner {
        height: auto;
        min-height: 56px;
        padding: 8px 16px 0;
        display: grid;
        grid-template-columns: minmax(0, 1fr) auto;
        gap: 4px 12px;
    }

    .l-nav__links {
        display: none;
        grid-row: 3;
        grid-column: 1 / -1;
        width: 100%;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 4px;
        padding: 4px 0 8px;
    }

    .l-nav__links--open {
        display: grid;
    }

    .l-nav__links li {
        min-width: 0;
    }

    .l-nav__menu-toggle {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        grid-column: 2;
        grid-row: 1;
        width: 44px;
        height: 44px;
        padding: 0;
        color: var(--text-h);
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius-sm);
        cursor: pointer;
    }

    .l-nav__menu-toggle:hover {
        background: var(--surface-alt);
        border-color: var(--border-strong);
    }

    .l-nav__menu-toggle:focus-visible {
        outline: 2px solid var(--border-focus);
        outline-offset: 2px;
    }

    .l-nav__link {
        display: flex;
        align-items: center;
        min-height: 44px;
        padding: 8px 10px;
        font-size: calc((12px) * var(--accessibility-text-scale, 1));
        white-space: normal;
    }

    .l-nav__actions {
        grid-column: 1 / -1;
        grid-row: 2;
        gap: 6px;
        justify-content: flex-end;
    }

    .l-nav__theme,
    .l-nav__signin,
    .l-nav__cta {
        min-height: 44px;
    }

    .l-nav__theme {
        width: 44px;
    }

    .l-nav__signin {
        font-size: calc((13px) * var(--accessibility-text-scale, 1));
    }

    .l-nav__cta {
        font-size: calc((13px) * var(--accessibility-text-scale, 1));
    }
}

@media (max-width: 360px) {
    .l-nav__inner {
        padding-inline: 12px;
    }

    .l-nav__brand {
        gap: 6px;
    }

    .l-nav__brand .al-brand-lockup__wordmark {
        font-size: 0.9rem;
    }

    .l-nav__cta {
        gap: 4px;
        padding-inline: 8px;
    }

    .l-nav__actions {
        gap: 3px;
    }

    .l-nav__signin {
        padding-inline: 5px;
        font-size: calc((12px) * var(--accessibility-text-scale, 1));
    }


    .l-nav__menu-toggle {
        width: 40px;
        height: 40px;
    }
}
</style>
