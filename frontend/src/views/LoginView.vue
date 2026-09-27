<script setup>
import { ref, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { login } from '../services/auth';
import { useAuth } from '../composables/useAuth';
import logo from '../assets/logo.png';

const router = useRouter();
const route = useRoute();
const { setUser } = useAuth();

const email    = ref('');
const password = ref('');
const error    = ref('');
const loading  = ref(false);

// Read redirect destination from query string; validate to same-origin paths only
const redirect = computed(() => {
    const r = route.query.redirect;
    if (typeof r === 'string' && r.startsWith('/') && !r.startsWith('//')) {
        return r;
    }
    return '/dashboard';
});

// Contextual label if arriving from a protected route
const contextLabel = computed(() => {
    const path = route.query.redirect;
    if (path === '/error-lens') return 'Sign in to continue to Error Lens.';
    if (path === '/docs-lens')  return 'Sign in to continue to Docs Lens.';
    if (path === '/dashboard')  return 'Sign in to continue to your dashboard.';
    return null;
});

async function handleLogin() {
    if (!email.value.trim() || !password.value) return;
    loading.value = true;
    error.value   = '';
    try {
        const user = await login({ email: email.value.trim(), password: password.value });
        setUser(user);
        router.push(redirect.value);
    } catch (err) {
        error.value = err.message || 'Something went wrong. Please try again.';
    } finally {
        loading.value = false;
    }
}
</script>

<template>
    <div class="auth-page">
        <div class="auth-page__inner">

            <!-- Brand -->
            <div class="auth-brand">
                <router-link to="/" class="al-brand-lockup al-brand-lockup--auth" aria-label="ArrowLens home">
                    <img :src="logo" alt="" aria-hidden="true" class="al-brand-lockup__mark" />
                    <span class="al-brand-lockup__wordmark">ArrowLens</span>
                </router-link>
            </div>

            <div class="auth-card">
                <!-- Context message when arriving from a protected route -->
                <div v-if="contextLabel" class="auth-context" role="status">
                    <svg aria-hidden="true" width="14" height="14" viewBox="0 0 14 14" fill="none">
                        <circle cx="7" cy="7" r="6" stroke="currentColor" stroke-width="1.2"/>
                        <path d="M7 5v3M7 9.5v.5" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
                    </svg>
                    {{ contextLabel }}
                </div>

                <header class="auth-card__header">
                    <h1 class="auth-card__title">Sign in</h1>
                    <p class="auth-card__sub">Welcome back to your workspace.</p>
                </header>

                <form class="auth-form" @submit.prevent="handleLogin" novalidate>
                    <div class="al-form-group">
                        <label for="login-email" class="al-label">Email</label>
                        <input
                            id="login-email"
                            v-model="email"
                            type="email"
                            class="al-input"
                            :class="{ 'al-input--error': error }"
                            placeholder="you@example.com"
                            autocomplete="email"
                            required
                        />
                    </div>

                    <div class="al-form-group">
                        <label for="login-password" class="al-label">Password</label>
                        <input
                            id="login-password"
                            v-model="password"
                            type="password"
                            class="al-input"
                            :class="{ 'al-input--error': error }"
                            placeholder="••••••••"
                            autocomplete="current-password"
                            required
                        />
                    </div>

                    <div v-if="error" class="al-status-error" role="alert">
                        {{ error }}
                    </div>

                    <button
                        type="submit"
                        class="al-btn al-btn--primary al-btn--lg auth-form__submit"
                        :disabled="loading"
                    >
                        <span v-if="loading" class="al-spinner" role="status" aria-label="Signing in…"></span>
                        <span v-else>Sign in</span>
                        <svg v-if="!loading" aria-hidden="true" class="al-btn__arrow" width="16" height="16" viewBox="0 0 16 16" fill="none">
                            <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </button>
                </form>

                <footer class="auth-card__footer">
                    <p>Don't have an account?
                        <router-link
                            :to="redirect !== '/dashboard' ? `/register?redirect=${redirect}` : '/register'"
                            class="auth-card__switch-link"
                        >Create one</router-link>
                    </p>
                </footer>
            </div>

            <!-- Subtle decorative aside -->
            <aside class="auth-aside" aria-hidden="true">
                <div class="auth-aside__signal">
                    <span class="auth-aside__tag">signal</span>
                    <div class="auth-aside__fields">
                        <span>Problem</span>
                        <span>Likely cause</span>
                        <span>Suggested fix</span>
                        <span>Verification</span>
                    </div>
                </div>
            </aside>

        </div>
    </div>
</template>

<style scoped>
.auth-page {
    min-height: 100svh;
    background: var(--bg);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: var(--space-8) var(--space-5);
}

.auth-page__inner {
    width: 100%;
    max-width: 440px;
    display: flex;
    flex-direction: column;
    gap: var(--space-8);
}

/* Brand */
.auth-brand {
    display: flex;
    justify-content: center;
}

/* Card */
.auth-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
}

.auth-context {
    display: flex;
    align-items: flex-start;
    gap: var(--space-2);
    padding: var(--space-3) var(--space-6);
    background: var(--accent-soft);
    border-bottom: 1px solid var(--accent-border);
    font-size: calc((13px) * var(--accessibility-text-scale, 1));
    color: var(--accent);
    line-height: 1.5;
}

.auth-card__header {
    padding: var(--space-8) var(--space-8) var(--space-5);
    border-bottom: 1px solid var(--border);
}

.auth-card__title {
    font-size: calc((22px) * var(--accessibility-text-scale, 1));
    font-weight: 500;
    letter-spacing: -0.02em;
    color: var(--text-h);
    margin-bottom: var(--space-1);
}

.auth-card__sub {
    font-size: calc((14px) * var(--accessibility-text-scale, 1));
    color: var(--text-muted);
}

/* Form */
.auth-form {
    padding: var(--space-6) var(--space-8);
    display: flex;
    flex-direction: column;
    gap: var(--space-5);
}

.auth-form__submit {
    width: 100%;
    justify-content: center;
    margin-top: var(--space-2);
}

/* Footer */
.auth-card__footer {
    padding: var(--space-5) var(--space-8);
    border-top: 1px solid var(--border);
    background: var(--bg);
}

.auth-card__footer p {
    font-size: calc((13px) * var(--accessibility-text-scale, 1));
    color: var(--text-muted);
    text-align: center;
}

.auth-card__switch-link {
    color: var(--accent);
    font-weight: 500;
    text-decoration: none;
}

.auth-card__switch-link:hover {
    text-decoration: underline;
}

.auth-card__switch-link:focus-visible {
    outline: 2px solid var(--accent);
    outline-offset: 2px;
    border-radius: 2px;
}

/* Decorative aside */
.auth-aside {
    display: flex;
    justify-content: center;
}

.auth-aside__signal {
    display: flex;
    align-items: center;
    gap: var(--space-4);
}

.auth-aside__tag {
    font-family: var(--mono);
    font-size: calc((10px) * var(--accessibility-text-scale, 1));
    color: var(--border-strong);
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.auth-aside__fields {
    display: flex;
    gap: var(--space-2);
    flex-wrap: wrap;
}

.auth-aside__fields span {
    font-family: var(--mono);
    font-size: calc((10px) * var(--accessibility-text-scale, 1));
    color: var(--text-muted);
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 3px;
    padding: 3px 8px;
}

/* Mobile */
@media (max-width: 480px) {
    .auth-card__header,
    .auth-form,
    .auth-card__footer {
        padding-left: var(--space-5);
        padding-right: var(--space-5);
    }
    .auth-aside {
        display: none;
    }
}
</style>
