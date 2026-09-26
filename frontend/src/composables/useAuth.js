/**
 * useAuth — ArrowLens authentication composable
 *
 * Single source of truth for auth state across all views.
 * Uses module-level reactive state so all consumers share
 * the same reference without Pinia.
 */

import { reactive, readonly } from 'vue';
import { getCurrentUser, logout as apiLogout } from '../services/auth';

// Module-level state — shared across all useAuth() calls
const state = reactive({
    user: null,       // { id, username, email } or null
    checked: false,   // true once the initial /me check has resolved
    loading: false,   // true while a check/logout is in progress
});

/**
 * Resolve the current session by calling /api/auth/me.
 * Called once on app boot (App.vue).
 * Safe to call multiple times — skips if already resolved.
 */
async function resolveAuth(force = false) {
    if (state.checked && !force) return;
    state.loading = true;
    try {
        const user = await getCurrentUser();
        state.user = user;
    } catch {
        // 401 or network error → not logged in
        state.user = null;
    } finally {
        state.checked = true;
        state.loading = false;
    }
}

/**
 * Set the user directly after a successful login/register response.
 * Avoids a redundant /me round-trip.
 */
function setUser(user) {
    state.user = user;
    state.checked = true;
}

/**
 * Log out: call the API, clear state.
 */
async function logout() {
    state.loading = true;
    try {
        await apiLogout();
    } catch {
        // Even if the API call fails, clear client state
    } finally {
        state.user = null;
        state.loading = false;
    }
}

/** Convenience: is the user currently authenticated? */
function isAuthenticated() {
    return !!state.user;
}

export function useAuth() {
    return {
        // Expose state as readonly — mutations go through the functions above
        state: readonly(state),
        resolveAuth,
        setUser,
        logout,
        isAuthenticated,
    };
}
