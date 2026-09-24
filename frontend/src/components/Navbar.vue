<script setup>
import { useRouter } from 'vue-router';
import { logout } from '../services/auth';

    const router = useRouter()

async function handleLogout() {

    // logout
    await logout()
    router.push("/login")
}

</script>

<template>
    <nav class="navbar">
        <div class="logo">Plutii</div>

        <div class="nav-links">
            <ul class="nav-list">
                <li class="nav-items">
                    <RouterLink to="/dashboard">Dashboard</RouterLink>
                </li>

                <li class="nav-items">
                    <RouterLink to="/notes">Notes</RouterLink>
                </li>

                <li class="nav-items">
                    <RouterLink to="/settings">Settings</RouterLink>
                </li>
            </ul>
        </div>

        <div class="nav-actions">
            <button class="logout" @click="handleLogout">
                Logout
            </button>
        </div>
    </nav>
</template>
    
<style scoped>
.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;

    padding: 14px 28px;
    margin: 16px;

    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(14px);

    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 16px;

    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.06);
}

/* Logo */

.logo {
    font-size: 1.5rem;
    font-weight: 800;
    letter-spacing: -0.5px;

    color: #42b883;
}

/* Navigation */

.nav-list {
    display: flex;
    align-items: center;
    gap: 8px;

    margin: 0;
    padding: 0;

    list-style: none;
}

.nav-items a {
    display: block;

    padding: 9px 14px;

    color: #555;
    text-decoration: none;

    font-size: 0.95rem;
    font-weight: 500;

    border-radius: 10px;

    transition:
        background 0.2s ease,
        color 0.2s ease,
        transform 0.2s ease;
}

.nav-items a:hover {
    color: #42b883;
    background: rgba(66, 184, 131, 0.1);

    transform: translateY(-1px);
}

/* Active route */

.nav-items a.router-link-active {
    color: #42b883;
    background: rgba(66, 184, 131, 0.12);
}

/* Logout */

.logout {
    border: none;

    padding: 9px 16px;

    border-radius: 10px;

    background: #f4f4f5;
    color: #444;

    font-size: 0.9rem;
    font-weight: 600;

    cursor: pointer;

    transition:
        background 0.2s ease,
        color 0.2s ease,
        transform 0.2s ease;
}

.logout:hover {
    background: #fee2e2;
    color: #dc2626;

    transform: translateY(-1px);
}

/* Mobile */

@media (max-width: 650px) {
    .navbar {
        flex-wrap: wrap;
        gap: 12px;

        padding: 12px 16px;
    }

    .nav-links {
        order: 3;
        width: 100%;
    }

    .nav-list {
        justify-content: center;
    }
}
</style>