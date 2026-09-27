<script setup>
import { onMounted, ref, computed } from 'vue';
import NoteCard from '../components/NoteCard.vue';
import NoteForm from '../components/NoteForm.vue';
import Navbar from '../components/Navbar.vue';
import { getNotes, createNote, updateNote, deleteNote, getAnalysisHistory, deleteAnalysis } from '../services/api.js';
import { useAuth } from '../composables/useAuth';

const { state: authState } = useAuth();

const notes = ref([]);
const selectedNote = ref(null);
const showForm = ref(false);
const loadError = ref('');
const loading = ref(true);

// History
const recentAnalyses = ref([]);
const historyLoading = ref(true);
const historyError = ref('');
const deletingAnalysisId = ref(null);

const greeting = computed(() => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good morning';
    if (hour < 18) return 'Good afternoon';
    return 'Good evening';
});

const username = computed(() => authState.user?.username || '');

async function loadNotes() {
    loading.value = true;
    loadError.value = '';
    try {
        notes.value = await getNotes();
    } catch (e) {
        loadError.value = e.message || 'Could not load notes.';
    } finally {
        loading.value = false;
    }
}

function openEditForm(note) {
    selectedNote.value = note;
    showForm.value = true;
}

function openCreateForm() {
    selectedNote.value = null;
    showForm.value = true;
}

async function saveNote(noteData) {
    if (selectedNote.value) {
        await updateNote(selectedNote.value.id, noteData);
    } else {
        await createNote(noteData);
    }
    await loadNotes();
    selectedNote.value = null;
    showForm.value = false;
}

async function handleDelete(id) {
    await deleteNote(id);
    await loadNotes();
}

function closeForm() {
    selectedNote.value = null;
    showForm.value = false;
}

async function loadRecentAnalyses() {
    try {
        recentAnalyses.value = await getAnalysisHistory();
    } catch (err) {
        console.error('Failed to load analysis history:', err);
    } finally {
        historyLoading.value = false;
    }
}

async function handleDeleteAnalysis(id) {
    if (deletingAnalysisId.value !== null) return;
    if (!window.confirm('Delete this analysis? This action cannot be undone.')) return;

    historyError.value = '';
    deletingAnalysisId.value = id;
    try {
        await deleteAnalysis(id);
        recentAnalyses.value = recentAnalyses.value.filter(item => item.id !== id);
    } catch (err) {
        historyError.value = err.message || 'Could not delete this analysis. Please try again.';
    } finally {
        deletingAnalysisId.value = null;
    }
}

onMounted(() => {
    loadNotes();
    loadRecentAnalyses();
});
</script>

<template>
    <div class="al-app-shell">
        <Navbar />

        <main class="al-app-main dashboard" id="main-content">
            <div class="al-container">

                <!-- ── WELCOME STUDIO BOARD HEADER ──────────────── -->
                <header class="db-header">
                    <div class="db-header__meta">
                        <span class="al-page-eyebrow">STUDIO BOARD // WORKSPACE</span>
                        <h1 class="db-greeting">
                            {{ greeting }}<span v-if="username">, {{ username }}</span>.
                        </h1>
                        <p class="db-sub">
                            Select an analytical aperture or pick up where your last engineering task left off.
                        </p>
                    </div>

                    <div class="db-header__stats" aria-hidden="true">
                        <div class="db-stat-item">
                            <span class="db-stat-val">{{ recentAnalyses.length }}</span>
                            <span class="db-stat-label">Analyses Logged</span>
                        </div>
                        <div class="db-stat-sep"></div>
                        <div class="db-stat-item">
                            <span class="db-stat-val">{{ notes.length }}</span>
                            <span class="db-stat-label">Notes Active</span>
                        </div>
                    </div>
                </header>

                <!-- ── THE 4 LENSES ──────────────────────────── -->
                <section class="db-section" aria-labelledby="lenses-heading">
                    <div class="db-section__header">
                        <div>
                            <span class="db-section__num">APERTURES</span>
                            <h2 id="lenses-heading" class="db-section__title">Choose a Lens</h2>
                        </div>
                        <span class="db-section__badge">4 Instruments Online</span>
                    </div>

                    <div class="db-lenses-grid">
                        <!-- ERROR LENS -->
                        <router-link to="/error-lens" class="db-lens-card db-lens-card--error">
                            <div class="db-lens-card__top">
                                <span class="db-lens-card__icon-badge al-lens-eyebrow__icon--error" aria-hidden="true">
                                    <svg width="13" height="13" viewBox="0 0 16 16" fill="none">
                                        <path d="M8 2.2L14.2 13.5H1.8L8 2.2Z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/>
                                        <path d="M8 6.2v3.3M8 11.2v.3" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
                                    </svg>
                                </span>
                                <span class="db-lens-card__tag">FAULT ISOLATION</span>
                            </div>
                            <div class="db-lens-card__body">
                                <h3 class="db-lens-card__title">Error Lens</h3>
                                <p class="db-lens-card__desc">
                                    Parse error tracebacks into cause, concrete code fix, and verification tests.
                                </p>
                            </div>
                            <div class="db-lens-card__footer">
                                <span class="db-lens-card__action">Launch Lens</span>
                                <svg class="db-lens-card__arrow" width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                                    <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
                                </svg>
                            </div>
                        </router-link>

                        <!-- DOCS LENS -->
                        <router-link to="/docs-lens" class="db-lens-card db-lens-card--docs">
                            <div class="db-lens-card__top">
                                <span class="db-lens-card__icon-badge al-lens-eyebrow__icon--docs" aria-hidden="true">
                                    <svg width="13" height="13" viewBox="0 0 16 16" fill="none">
                                        <path d="M3.5 2.5h6l3 3v8a1 1 0 0 1-1 1h-8a1 1 0 0 1-1-1v-10a1 1 0 0 1 1-1z" stroke="currentColor" stroke-width="1.3"/>
                                        <path d="M9.5 2.5v3h3M5.5 8h5M5.5 10.5h3.5" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
                                    </svg>
                                </span>
                                <span class="db-lens-card__tag">DISTILLATION</span>
                            </div>
                            <div class="db-lens-card__body">
                                <h3 class="db-lens-card__title">Docs Lens</h3>
                                <p class="db-lens-card__desc">
                                    Fetch live documentation URLs or paste raw specs to extract key concepts and code examples.
                                </p>
                            </div>
                            <div class="db-lens-card__footer">
                                <span class="db-lens-card__action">Launch Lens</span>
                                <svg class="db-lens-card__arrow" width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                                    <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
                                </svg>
                            </div>
                        </router-link>

                        <!-- PLAN LENS -->
                        <router-link to="/plan-lens" class="db-lens-card db-lens-card--plan">
                            <div class="db-lens-card__top">
                                <span class="db-lens-card__icon-badge al-lens-eyebrow__icon--plan" aria-hidden="true">
                                    <svg width="13" height="13" viewBox="0 0 16 16" fill="none">
                                        <circle cx="3.5" cy="4" r="1.5" stroke="currentColor" stroke-width="1.3"/>
                                        <circle cx="12.5" cy="12" r="1.5" stroke="currentColor" stroke-width="1.3"/>
                                        <path d="M5 4h3.5a2.5 2.5 0 0 1 2.5 2.5v3a2.5 2.5 0 0 0 2.5 2.5H11" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
                                    </svg>
                                </span>
                                <span class="db-lens-card__tag">ROADMAP ENGINE</span>
                            </div>
                            <div class="db-lens-card__body">
                                <h3 class="db-lens-card__title">Plan Lens</h3>
                                <p class="db-lens-card__desc">
                                    Transform raw notes into step-by-step implementation milestones with dependency maps.
                                </p>
                            </div>
                            <div class="db-lens-card__footer">
                                <span class="db-lens-card__action">Launch Lens</span>
                                <svg class="db-lens-card__arrow" width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                                    <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
                                </svg>
                            </div>
                        </router-link>

                        <!-- CODEBASE LENS -->
                        <router-link to="/codebase-lens" class="db-lens-card db-lens-card--codebase">
                            <div class="db-lens-card__top">
                                <span class="db-lens-card__icon-badge al-lens-eyebrow__icon--codebase" aria-hidden="true">
                                    <svg width="13" height="13" viewBox="0 0 16 16" fill="none">
                                        <rect x="2" y="2.5" width="5" height="4" rx="1" stroke="currentColor" stroke-width="1.3"/>
                                        <rect x="9" y="2.5" width="5" height="4" rx="1" stroke="currentColor" stroke-width="1.3"/>
                                        <rect x="5.5" y="9.5" width="5" height="4" rx="1" stroke="currentColor" stroke-width="1.3"/>
                                        <path d="M4.5 6.5v1.5a1 1 0 0 0 1 1h5a1 1 0 0 0 1-1V6.5" stroke="currentColor" stroke-width="1.2"/>
                                    </svg>
                                </span>
                                <span class="db-lens-card__tag">TOPOLOGY SCAN</span>
                            </div>
                            <div class="db-lens-card__body">
                                <h3 class="db-lens-card__title">Codebase Lens</h3>
                                <p class="db-lens-card__desc">
                                    Inspect project architecture, graph module dependencies, and search codebase structure.
                                </p>
                            </div>
                            <div class="db-lens-card__footer">
                                <span class="db-lens-card__action">Launch Lens</span>
                                <svg class="db-lens-card__arrow" width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                                    <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
                                </svg>
                            </div>
                        </router-link>
                    </div>
                </section>

                <!-- ── 02 RECENT ACTIVITY ───────────────────────── -->
                <section class="db-section" id="recent-activity" aria-labelledby="activity-heading">
                    <div class="db-section__header">
                        <div>
                            <span class="db-section__num">02 / AUDIT LOG</span>
                            <h2 id="activity-heading" class="db-section__title">Recent Activity</h2>
                        </div>
                    </div>

                    <div v-if="historyError" class="al-status-error" role="alert">
                        {{ historyError }}
                    </div>

                    <!-- Loading -->
                    <div v-if="historyLoading" class="al-loading-state">
                        <div class="al-spinner" role="status" aria-label="Loading recent activity"></div>
                        <span>Scanning history…</span>
                    </div>

                    <!-- Empty -->
                    <div v-else-if="recentAnalyses.length === 0" class="al-empty-state">
                        <div class="al-empty-state__icon" aria-hidden="true">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                                <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.5"/>
                                <path d="M12 7v5l3 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                            </svg>
                        </div>
                        <div class="al-empty-state__title">NO SIGNAL YET</div>
                        <p class="al-empty-state__desc">
                            Your analyzed errors, documentation distillations, and implementation roadmaps will appear here.
                        </p>
                    </div>

                    <!-- Activity List -->
                    <div v-else class="db-activity-list" role="list">
                        <div
                            v-for="item in recentAnalyses"
                            :key="item.id"
                            class="db-activity-item"
                            role="listitem"
                        >
                            <router-link
                                :to="`/analysis/${item.id}`"
                                class="db-activity-item__link"
                            >
                                <div class="db-activity-item__lens" :class="`db-activity-item__lens--${item.lens_type}`">
                                    <span>{{ item.lens_type }}</span>
                                </div>

                                <div class="db-activity-item__content">
                                    <h3 class="db-activity-item__query">
                                        {{ item.input }}
                                    </h3>
                                    <span class="db-activity-item__date">
                                        {{ new Date(item.created_at).toLocaleString() }}
                                    </span>
                                </div>

                                <svg class="db-activity-item__arrow" width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                                    <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
                                </svg>
                            </router-link>

                            <button
                                type="button"
                                class="db-activity-item__delete"
                                aria-label="Delete analysis"
                                :title="deletingAnalysisId === item.id ? 'Deleting analysis' : 'Delete analysis'"
                                :aria-busy="deletingAnalysisId === item.id"
                                :disabled="deletingAnalysisId !== null"
                                @click="handleDeleteAnalysis(item.id)"
                            >
                                <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                                    <path d="M3 4.5h10M6 4.5V3h4v1.5m2 0-.6 8H4.6l-.6-8M6.5 7v3.5M9.5 7v3.5" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>
                                </svg>
                            </button>
                        </div>
                    </div>
                </section>

                <!-- ── 03 NOTES & SCRATCHPAD ─────────────────────── -->
                <section class="db-section" id="notes" aria-labelledby="notes-heading">
                    <div class="db-section__header">
                        <div>
                            <span class="db-section__num">03 / SCRATCHPAD</span>
                            <h2 id="notes-heading" class="db-section__title">Developer Notes</h2>
                        </div>
                        <button class="al-btn al-btn--primary al-btn--sm" @click="openCreateForm">
                            + New Note
                        </button>
                    </div>

                    <!-- Loading -->
                    <div v-if="loading" class="al-loading-state">
                        <div class="al-spinner" role="status" aria-label="Loading notes"></div>
                        <span>Loading notes…</span>
                    </div>

                    <!-- Error -->
                    <div v-else-if="loadError" class="al-status-error" role="alert">
                        {{ loadError }}
                    </div>

                    <!-- Empty -->
                    <div v-else-if="notes.length === 0" class="al-empty-state">
                        <div class="al-empty-state__icon" aria-hidden="true">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                                <path d="M4 4h16v16H4z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
                                <path d="M8 8h8M8 12h8M8 16h4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
                            </svg>
                        </div>
                        <div class="al-empty-state__title">NO NOTES YET</div>
                        <p class="al-empty-state__desc">
                            Capture an idea or implementation note and turn it into an architectural roadmap.
                        </p>
                        <button class="al-btn al-btn--secondary al-btn--sm" style="margin-top: 12px" @click="openCreateForm">
                            + Create First Note
                        </button>
                    </div>

                    <!-- Notes Grid -->
                    <div v-else class="db-notes-grid">
                        <NoteCard
                            v-for="note in notes"
                            :key="note.id"
                            :note="note"
                            @edit="openEditForm"
                            @delete="handleDelete"
                        />
                    </div>

                    <!-- Form Modal -->
                    <NoteForm
                        v-if="showForm"
                        :note="selectedNote"
                        @save="saveNote"
                        @cancel="closeForm"
                    />
                </section>

            </div>
        </main>
    </div>
</template>

<style scoped>
.dashboard {
    max-width: var(--max-w);
}

/* ── Studio Board Header ─────────────────────────────────────── */
.db-header {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: var(--space-6);
    padding-bottom: var(--space-8);
    border-bottom: 1px solid var(--border);
    margin-bottom: var(--space-10);
    position: relative;
}

.db-header__meta {
    max-width: 680px;
}

.db-greeting {
    font-size: clamp(1.8rem, 3.5vw, 2.5rem);
    font-weight: 600;
    letter-spacing: -0.03em;
    color: var(--text-h);
    margin: var(--space-1) 0 var(--space-2);
}

.db-sub {
    font-size: 0.95rem;
    color: var(--text-muted);
    line-height: 1.55;
}

.db-header__stats {
    display: flex;
    align-items: center;
    gap: var(--space-5);
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: var(--space-3) var(--space-5);
    box-shadow: var(--shadow-sm);
}

.db-stat-item {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

.db-stat-val {
    font-family: var(--mono);
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text-h);
    line-height: 1.1;
}

.db-stat-label {
    font-size: 0.725rem;
    color: var(--text-muted);
}

.db-stat-sep {
    width: 1px;
    height: 24px;
    background: var(--border);
}

/* ── Section Standards ───────────────────────────────────────── */
.db-section {
    margin-bottom: var(--space-12);
}

.db-section__header {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    margin-bottom: var(--space-6);
}

.db-section__num {
    font-family: var(--mono);
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: var(--text-muted);
    display: block;
    margin-bottom: 2px;
}

.db-section__title {
    font-family: var(--heading);
    font-size: 1.35rem;
    font-weight: 600;
    letter-spacing: -0.02em;
    color: var(--text-h);
    margin: 0;
}

.db-section__badge {
    font-family: var(--mono);
    font-size: 0.7rem;
    color: var(--text-muted);
    background: var(--surface-alt);
    border: 1px solid var(--border);
    padding: 3px 8px;
    border-radius: var(--radius-sm);
}

/* ── 4 Unified Lens Cards Grid ───────────────────────────────── */
.db-lenses-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: var(--space-5);
}

.db-lens-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: var(--space-6);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    text-decoration: none !important;
    color: var(--text);
    box-shadow: var(--shadow-sm);
    transition: transform var(--duration-fast), border-color var(--duration-fast), box-shadow var(--duration-fast);
    position: relative;
    border-top: 3px solid var(--border-strong);
}

.db-lens-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

.db-lens-card:hover .db-lens-card__arrow {
    transform: translateX(3px);
}

.db-lens-card--error {
    border-top-color: var(--lens-error);
}
.db-lens-card--error:hover {
    border-color: var(--lens-error-border);
    border-top-color: var(--lens-error);
}

.db-lens-card--docs {
    border-top-color: var(--lens-docs);
}
.db-lens-card--docs:hover {
    border-color: var(--lens-docs-border);
    border-top-color: var(--lens-docs);
}

.db-lens-card--plan {
    border-top-color: var(--lens-plan);
}
.db-lens-card--plan:hover {
    border-color: var(--lens-plan-border);
    border-top-color: var(--lens-plan);
}

.db-lens-card--codebase {
    border-top-color: var(--lens-codebase);
}
.db-lens-card--codebase:hover {
    border-color: var(--lens-codebase-border);
    border-top-color: var(--lens-codebase);
}

.db-lens-card__top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: var(--space-4);
}

.db-lens-card__icon-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 26px;
    height: 26px;
    border-radius: var(--radius-sm);
    flex-shrink: 0;
}

.db-lens-card__tag {
    font-family: var(--mono);
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    color: var(--text-muted);
}

.db-lens-card__body {
    flex: 1;
    display: flex;
    flex-direction: column;
}


.db-lens-card__title {
    font-family: var(--heading);
    font-size: 1.15rem;
    font-weight: 600;
    letter-spacing: -0.015em;
    color: var(--text-h);
    margin: 0 0 var(--space-2);
}

.db-lens-card__desc {
    font-size: 0.85rem;
    line-height: 1.55;
    color: var(--text-muted);
    margin: 0 0 var(--space-5);
}

.db-lens-card__footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-top: var(--space-3);
    border-top: 1px dashed var(--border);
    font-family: var(--mono);
    font-size: 0.775rem;
    font-weight: 600;
    color: var(--accent);
}

.db-lens-card__arrow {
    transition: transform var(--duration-fast) var(--ease-out);
}

/* ── Recent Activity ─────────────────────────────────────────── */
.db-activity-list {
    display: flex;
    flex-direction: column;
    gap: var(--space-2);
}

.db-activity-item {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    padding: var(--space-4) var(--space-5);
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    color: var(--text);
    box-shadow: var(--shadow-sm);
    transition: border-color var(--duration-fast), transform var(--duration-fast);
}

.db-activity-item:hover {
    border-color: var(--border-strong);
    transform: translateX(2px);
}

.db-activity-item__link {
    display: flex;
    flex: 1;
    align-items: center;
    gap: var(--space-4);
    min-width: 0;
    color: inherit;
    text-decoration: none !important;
}

.db-activity-item__delete {
    display: inline-flex;
    flex: 0 0 32px;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    padding: 0;
    border: 1px solid transparent;
    border-radius: var(--radius-sm);
    background: transparent;
    color: var(--text-muted);
    cursor: pointer;
    transition: color var(--duration-fast), background-color var(--duration-fast);
}

.db-activity-item__delete:hover:not(:disabled) {
    background: var(--error-bg);
    color: var(--error);
}

.db-activity-item__delete:disabled {
    cursor: wait;
    opacity: 0.55;
}

.db-activity-item__lens {
    font-family: var(--mono);
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 3px 8px;
    border-radius: var(--radius-sm);
    border: 1px solid var(--border);
    background: var(--surface-alt);
    color: var(--text-muted);
    flex-shrink: 0;
}

.db-activity-item__lens--error {
    background: var(--lens-error-bg);
    color: var(--lens-error);
    border-color: var(--lens-error-border);
}

.db-activity-item__lens--docs {
    background: var(--lens-docs-bg);
    color: var(--lens-docs);
    border-color: var(--lens-docs-border);
}

.db-activity-item__lens--plan {
    background: var(--lens-plan-bg);
    color: var(--lens-plan);
    border-color: var(--lens-plan-border);
}

.db-activity-item__lens--codebase {
    background: var(--lens-codebase-bg);
    color: var(--lens-codebase);
    border-color: var(--lens-codebase-border);
}

.db-activity-item__content {
    flex: 1;
    min-width: 0;
}

.db-activity-item__query {
    font-size: 0.885rem;
    font-weight: 550;
    color: var(--text-h);
    margin: 0 0 2px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.db-activity-item__date {
    font-family: var(--mono);
    font-size: 0.725rem;
    color: var(--text-muted);
}

.db-activity-item__arrow {
    color: var(--text-muted);
    flex-shrink: 0;
}

/* ── Notes Grid ──────────────────────────────────────────────── */
.db-notes-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: var(--space-5);
}

/* ── Responsive ──────────────────────────────────────────────── */
@media (max-width: 1100px) {
    .db-lenses-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 640px) {
    .db-lenses-grid {
        grid-template-columns: 1fr;
    }
    .db-header {
        flex-direction: column;
        align-items: flex-start;
    }
    .db-notes-grid {
        grid-template-columns: 1fr;
    }
    .db-activity-item {
        padding: var(--space-3);
    }
    .db-activity-item__link {
        gap: var(--space-2);
    }
}
</style>
