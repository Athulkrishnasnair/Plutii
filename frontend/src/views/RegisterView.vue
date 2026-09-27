<script setup>
import { ref, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { register } from '../services/auth';
import { useAuth } from '../composables/useAuth';
import logo from '../assets/logo.png';


const router = useRouter();
const route = useRoute();
const { setUser } = useAuth();

const username = ref('');
const email = ref('');
const password = ref('');
const showPassword = ref(false);
const error = ref('');
const loading = ref(false);

const redirect = computed(() => {
    const r = route.query.redirect;
    if (typeof r === 'string' && r.startsWith('/') && !r.startsWith('//')) {
        return r;
    }
    return '/dashboard';
});

async function handleRegister() {
    if (!username.value.trim() || !email.value.trim() || !password.value) return;
    loading.value = true;
    error.value = '';

    try {
        const user = await register({
            username: username.value.trim(),
            email: email.value.trim(),
            password: password.value,
        });
        setUser(user);
        router.push(redirect.value);
    } catch (err) {
        error.value = err.message || 'Registration failed. Please check your details and try again.';
    } finally {
        loading.value = false;
    }
}
</script>

<template>
    <div class="auth-page">
        <div class="auth-page__inner">

            <!-- Brand Header -->
            <div class="auth-brand">
                <router-link to="/" class="al-brand-lockup al-brand-lockup--auth" aria-label="ArrowLens home">
                    <img :src="logo" alt="" aria-hidden="true" class="al-brand-lockup__mark" />
                    <span class="al-brand-lockup__wordmark">ArrowLens</span>

                </router-link>
            </div>

            <div class="auth-card">
                <header class="auth-card__header">
                    <span class="auth-eyebrow">REGISTRATION // NEW WORKSPACE</span>
                    <h1 class="auth-card__title">Create Developer Account</h1>
                    <p class="auth-card__sub">Get started with the full 4-lens developer instrument.</p>
                </header>

                <form class="auth-form" @submit.prevent="handleRegister" novalidate>
                    <div class="al-form-group">
                        <label for="reg-username" class="al-label">Username</label>
                        <input
                            id="reg-username"
                            v-model="username"
                            type="text"
                            class="al-input"
                            :class="{ 'al-input--error': error && !username.trim() }"
                            placeholder="your_handle"
                            autocomplete="username"
                            required
                            autofocus
                        />
                    </div>

                    <div class="al-form-group">
                        <label for="reg-email" class="al-label">Email Address</label>
                        <input
                            id="reg-email"
                            v-model="email"
                            type="email"
                            class="al-input"
                            :class="{ 'al-input--error': error && !email.trim() }"
                            placeholder="you@domain.com"
                            autocomplete="email"
                            required
                        />
                    </div>

                    <div class="al-form-group">
                        <div class="pwd-label-row">
                            <label for="reg-password" class="al-label">Password</label>
                            <button
                                type="button"
                                class="pwd-toggle-btn"
                                @click="showPassword = !showPassword"
                                :aria-label="showPassword ? 'Hide password' : 'Show password'"
                            >
                                {{ showPassword ? 'Hide' : 'Show' }}
                            </button>
                        </div>
                        <input
                            id="reg-password"
                            v-model="password"
                            :type="showPassword ? 'text' : 'password'"
                            class="al-input"
                            :class="{ 'al-input--error': error && !password }"
                            placeholder="••••••••"
                            autocomplete="new-password"
                            required
                        />
                    </div>

                    <div v-if="error" class="al-status-error" role="alert">
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true" style="flex-shrink: 0; margin-top: 2px">
                            <circle cx="8" cy="8" r="7" stroke="currentColor" stroke-width="1.3"/>
                            <path d="M8 5v3.5M8 11v.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                        </svg>
                        <span>{{ error }}</span>
                    </div>

                    <button
                        type="submit"
                        class="al-btn al-btn--primary al-btn--lg auth-submit-btn"
                        :disabled="loading || !username.trim() || !email.trim() || !password"
                    >
                        <span v-if="loading" class="al-spinner" role="status" aria-label="Creating account…"></span>
                        <span v-else>Initialize Workspace</span>
                        <svg v-if="!loading" aria-hidden="true" class="al-btn__arrow" width="16" height="16" viewBox="0 0 16 16" fill="none">
                            <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </button>
                </form>

                <footer class="auth-card__footer">
                    <p>Already have an account?
                        <router-link
                            :to="redirect !== '/dashboard' ? `/login?redirect=${redirect}` : '/login'"
                            class="auth-card__switch-link"
                        >Sign in</router-link>
                    </p>
                </footer>
            </div>

            <!-- Technical Annotation -->
            <div class="auth-calibration-note" aria-hidden="true">
                <span>[SESSION: LOCAL_PERSISTENCE]</span>
                <span>[ENV: FLASK_SESSION]</span>
            </div>

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
    padding: var(--space-8) var(--space-4);
    background-image:
        radial-gradient(var(--border) 1px, transparent 1px);
    background-size: 32px 32px;
}

.auth-page__inner {
    width: 100%;
    max-width: 440px;
    display: flex;
    flex-direction: column;
    gap: var(--space-6);
}

.auth-brand {
    display: flex;
    justify-content: center;
}

.auth-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-md);
    overflow: hidden;
}

.auth-card__header {
    padding: var(--space-6) var(--space-6) var(--space-4);
    border-bottom: 1px solid var(--border);
    background: var(--surface-alt);
}

.auth-eyebrow {
    font-family: var(--mono);
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: var(--text-muted);
    display: block;
    margin-bottom: 4px;
}

.auth-card__title {
    font-family: var(--heading);
    font-size: 1.35rem;
    font-weight: 600;
    color: var(--text-h);
    margin: 0 0 2px;
}

.auth-card__sub {
    font-size: 0.85rem;
    color: var(--text-muted);
}

.auth-form {
    padding: var(--space-6);
    display: flex;
    flex-direction: column;
    gap: var(--space-4);
}

.pwd-label-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.pwd-toggle-btn {
    font-family: var(--mono);
    font-size: 0.7rem;
    color: var(--accent);
    background: none;
    border: none;
    cursor: pointer;
    padding: 0;
}

.pwd-toggle-btn:hover {
    text-decoration: underline;
}

.auth-submit-btn {
    width: 100%;
    margin-top: var(--space-2);
}

.auth-card__footer {
    padding: var(--space-4) var(--space-6);
    border-top: 1px solid var(--border);
    background: var(--surface-alt);
    text-align: center;
}

.auth-card__footer p {
    font-size: 0.85rem;
    color: var(--text-muted);
}

.auth-card__switch-link {
    color: var(--accent);
    font-weight: 600;
    text-decoration: none;
    margin-left: 4px;
}

.auth-card__switch-link:hover {
    text-decoration: underline;
}

.auth-calibration-note {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-family: var(--mono);
    font-size: 0.65rem;
    color: var(--text-muted);
    padding: 0 var(--space-2);
}
</style>
