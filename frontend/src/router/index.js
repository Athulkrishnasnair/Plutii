import {createRouter, createWebHistory} from "vue-router";

// Configure vue-router
const router = createRouter({
    history: createWebHistory(),

    // Define the routes
    routes: [
        {
            path: "/",
            component: () => import("../views/LandingView.vue")
        },
        {
            path: "/login",
            component: () => import("../views/LoginView.vue")
        },
        {
            path: "/register",
            component: () => import("../views/RegisterView.vue")
        },
        {
            path: "/dashboard",
            component: () => import("../views/DashboardView.vue")
        }
    ]
});

export default router;

