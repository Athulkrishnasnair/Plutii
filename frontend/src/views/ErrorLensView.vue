<template>
    <main class="error-lens">
        <header class="page-header">
             <div>
                <p class="eyebrow">ARROWLENS</p>
                <h1>Error Lens</h1>
                <p>
                    Understand errors, identify likely causes,
                    and work toward a verified fix.
                </p>
            </div>
        </header>
        
        <section class="workspace">
            <form @submit.prevent="handleAnalyze" class="input-panel">
                <label for="error">
                    Error message
                </label>

                <textarea  id="error"
                    v-model="error"
                    placeholder="Paste the error message here..."
                    required
                ></textarea>

                <label for="code">
                    Relevant Code
                </label>

                <textarea  id="code"
                    v-model="code"
                    placeholder="Paste the relevant code here..."
                ></textarea>

                <label for="context">
                    Context
                </label>

                <textarea  id="context"
                    v-model="context"
                        placeholder="What were you trying to do?"
                ></textarea>

                <button type="submit"
                :disabled="loading"
                > 
                {{ loading ? "Analyzing..." : "Analyze Error" }}
                </button>

                <p class="error-message" v-if="errorMessage">
                    {{ errorMessage }}
                </p>
            </form>

            <!-- Results -->

            <section class="result-panel">
                <div class="empty-state" v-if="loading">
                    Analyzing your error...
                </div>

                 <div v-else-if="!result" class="empty-state">
                    <h2>Analysis</h2>
                    <p>
                        Your analysis will appear here.
                    </p>
                </div>

                <div v-else class="analysis">
                    <section>
                        <h2>Problem</h2>
                        <p>{{ result.problem }}</p>
                    </section>

                    <section>
                        <h2>Likely Cause</h2>
                        <p>{{ result.cause }}</p>
                    </section>

                    <section>
                        <h2>Suggested Fix</h2>
                        <p>{{ result.fix }}</p>
                    </section>

                    <section>
                        <h2>Verification</h2>

                        <ul>
                            <li
                                v-for="step in result.verification"
                                :key="step"
                            >
                                {{ step }}
                            </li>
                        </ul>
                    </section>
                </div>
            </section>

        </section>
    </main>
</template>

<script setup>
import { ref } from 'vue';
import { analyzeError } from '../services/api';

const error = ref('');
const code = ref('');
const context = ref('');

const result = ref(null);
const loading = ref(false);
const errorMessage = ref('');

async function handleAnalyze() {
    loading.value = true;
    errorMessage.value = '';
    result.value = null;

    try {
        result.value = await analyzeError(
            error.value,
            code.value,
            context.value
        );
    } catch (error) {
        errorMessage.value = error.message;
    } finally {
        loading.value = false;
    }
}

</script>


<style scoped>
.error-lens {
    max-width: 1200px;
    margin: 0 auto;
    padding: 40px 24px;
}

.page-header {
    margin-bottom: 32px;
}

.eyebrow {
    margin: 0 0 8px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.12em;
}

.page-header h1 {
    margin: 0;
    font-size: 2.2rem;
}

.page-header p {
    color: #666;
}

.workspace {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
}

.input-panel,
.result-panel {
    padding: 24px;
    border: 1px solid #e5e5e5;
    border-radius: 16px;
    background: white;
}

.input-panel {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

label {
    font-weight: 600;
    margin-top: 8px;
}

textarea {
    min-height: 110px;
    padding: 12px;
    border: 1px solid #d8d8d8;
    border-radius: 10px;
    resize: vertical;
    font: inherit;
}

button {
    margin-top: 10px;
    padding: 12px 18px;
    border: none;
    border-radius: 10px;
    background: #222;
    color: white;
    font-weight: 600;
    cursor: pointer;
}

button:disabled {
    opacity: 0.6;
    cursor: wait;
}

.result-panel {
    min-height: 500px;
}

.empty-state {
    color: #777;
}

.analysis {
    display: flex;
    flex-direction: column;
    gap: 24px;
}

.analysis h2 {
    margin-bottom: 8px;
    font-size: 1rem;
}

.analysis p {
    margin: 0;
    line-height: 1.6;
}

.analysis ul {
    margin: 0;
    padding-left: 20px;
}

.analysis li {
    margin-bottom: 8px;
}

.error-message {
    color: #c0392b;
}

@media (max-width: 800px) {
    .workspace {
        grid-template-columns: 1fr;
    }
}
</style>