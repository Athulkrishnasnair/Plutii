<script setup>
import { computed } from 'vue';
import { useAuth } from '../composables/useAuth';
import logo from '../assets/logo.png';

const { isAuthenticated } = useAuth();
const authed = computed(() => isAuthenticated());
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
            <ul class="l-nav__links" role="list">
                <li><a href="#error-lens" class="l-nav__link">Error Lens</a></li>
                <li><a href="#docs-lens" class="l-nav__link">Docs Lens</a></li>
            </ul>

            <!-- Auth actions: changes based on session state -->
            <div class="l-nav__actions">
                <template v-if="authed">
                    <router-link to="/dashboard" class="l-nav__cta">
                        Dashboard
                        <svg aria-hidden="true" width="14" height="14" viewBox="0 0 14 14" fill="none">
                            <path d="M2.5 7h9M8 3.5 11.5 7 8 10.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </router-link>
                </template>
                <template v-else>
                    <router-link to="/login" class="l-nav__signin">Sign in</router-link>
                    <router-link to="/register" class="l-nav__cta">
                        Get started
                        <svg aria-hidden="true" width="14" height="14" viewBox="0 0 14 14" fill="none">
                            <path d="M2.5 7h9M8 3.5 11.5 7 8 10.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
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
    padding: 0 32px;
    height: 56px;
    display: flex;
    align-items: center;
    gap: 32px;
}

.l-nav__brand {
    flex-shrink: 0;
}

.l-nav__links {
    display: flex;
    align-items: center;
    gap: 4px;
    list-style: none;
    margin: 0;
    padding: 0;
    flex: 1;
}

.l-nav__link {
    font-size: calc((14px) * var(--accessibility-text-scale, 1));
    color: var(--text);
    text-decoration: none;
    padding: 6px 10px;
    border-radius: 5px;
    transition: color 0.18s, background 0.18s;
}

.l-nav__link:hover {
    color: var(--text-h);
    background: var(--l-surface);
}

.l-nav__link:focus-visible {
    outline: 2px solid var(--accent);
    outline-offset: 2px;
}
:root[data-theme="dark"] .l-nav__cta {
     background: var(--text-h);
     color: var(--bg);
}

:root[data-theme="dark"] .l-nav__cta:hover {
     background: #e8e8f0;
    font-size: calc((14px) * var(--accessibility-text-scale, 1));
    color: var(--text);
    text-decoration: none;
    padding: 6px 10px;
    border-radius: 5px;
    transition: color 0.18s;
}

.l-nav__signin:hover {
    color: var(--text-h);
}

.l-nav__signin:focus-visible {
    outline: 2px solid var(--accent);
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
    padding: 7px 14px;
    border-radius: 6px;
    transition: background 0.18s, gap 0.18s;
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
        padding: 0 20px;
        gap: 16px;
    }
    .l-nav__links {
        display: none;
    }
    .l-nav__signin {
        display: none;
    }
    .l-nav__cta {
        padding: 7px 12px;
        font-size: calc((13px) * var(--accessibility-text-scale, 1));
    }
}
</style>
