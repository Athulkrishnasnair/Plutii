import { createRouter, createWebHistory } from 'vue-router';
import { useAuth } from '../composables/useAuth';
// simport PlanLensView from "../views/PlanLensView.vue";


const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: () => import('../views/LandingView.vue'),
        },
        {
            path: '/login',
            component: () => import('../views/LoginView.vue'),
            meta: { guestOnly: true },
        },
        {
            path: '/register',
            component: () => import('../views/RegisterView.vue'),
            meta: { guestOnly: true },
        },
        {
            path: '/dashboard',
            component: () => import('../views/DashboardView.vue'),
            meta: { requiresAuth: true },
        },
        {
            path: '/error-lens',
            name: 'error-lens',
            component: () => import('../views/ErrorLensView.vue'),
            meta: { requiresAuth: true },
        },
        {
        path: '/plan-lens',
        component: () => import('../views/PlanLensView.vue'),
        meta: { requiresAuth: true }
        }
        ,
        {
            path: '/docs-lens',
            name: 'docs-lens',
            component: () => import('../views/DocsLensView.vue'),
            meta: { requiresAuth: true },
        },
        {
            path: '/analysis/:id',
            component: () => import('../views/AnalysisHistoryView.vue'),
            meta: {
                requiresAuth: true
            }
        },
        {
            path: '/codebase-lens',
            component: () => import('../views/CodebaseLensView.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/:pathMatch(.*)*',
            name: 'not-found',
            component: () => import('../views/NotFoundView.vue')
        }
    ],
});

router.beforeEach(async (to) => {
    const { state, resolveAuth, isAuthenticated } = useAuth();

    // Wait for the initial auth check before any navigation decision
    if (!state.checked) {
        await resolveAuth();
    }

    const authed = isAuthenticated();

    // Protected route — redirect to login with return destination
    if (to.meta.requiresAuth && !authed) {
        return {
            path: '/login',
            query: { redirect: to.fullPath },
        };
    }

    // Already authenticated — no need to visit login/register
    if (to.meta.guestOnly && authed) {
        return { path: '/dashboard' };
    }

    // All clear
    return true;
});

export default router;
