<template>
    <main>
        <h1>Login</h1>

        <form @submit.prevent="handleLogin">
            <input type="text"
                v-model="email"
                placeholder="Type Email..."
            >

            <input type="password"
                v-model="password"
                placeholder="Pasword..."
            >
            <p v-if="error">{{ error }}</p>

            <button type="submit">Login</button>
        </form>
    </main>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from "vue-router"
import { login } from '../services/auth';

const router = useRouter();
const email = ref('');
const password = ref('');
const error = ref('');

async function handleLogin() {
    error.value = '';

    //  make a request
    try {
        const user = await login({
            email: email.value,
            password: password.value
        })

        router.push("/dashboard");
    }
    catch (err) 
    {
        error.value = err.message;
    }
}


</script>