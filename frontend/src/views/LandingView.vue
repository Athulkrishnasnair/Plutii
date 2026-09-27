<script setup>
import { onMounted, onUnmounted, computed } from 'vue';
import LandingNavbar from '../components/LandingNavbar.vue';
import { useAuth } from '../composables/useAuth';
import logo from '../assets/logo.png';

const { isAuthenticated } = useAuth();
const authed = computed(() => isAuthenticated());

// Auth-aware CTA targets: authenticated users go straight to the tool;
// anonymous users are sent to login with the intended destination.
const errorLensTarget = computed(() =>
    authed.value ? '/error-lens' : '/login?redirect=/error-lens'
);
const docsLensTarget = computed(() =>
    authed.value ? '/docs-lens' : '/login?redirect=/docs-lens'
);
const primaryCTA = computed(() =>
    authed.value ? '/dashboard' : '/register'
);
const primaryCTALabel = computed(() =>
    authed.value ? 'Go to dashboard' : 'Start for free'
);

// IntersectionObserver for section entrance animations
let observer = null;

onMounted(() => {
    const targets = document.querySelectorAll('.l-reveal');
    observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('l-reveal--visible');
                    observer.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.08 }
    );
    targets.forEach((el) => observer.observe(el));
});

onUnmounted(() => {
    if (observer) observer.disconnect();
});
</script>

<template>
    <div class="landing">
        <LandingNavbar />

        <main id="main-content">

            <!-- ── 01 INTRO ─────────────────────────────────────── -->
            <section class="l-section l-intro" aria-labelledby="intro-heading">
                <div class="l-inner">
                    <div class="l-section__num" aria-hidden="true">01</div>

                    <div class="l-intro__body l-reveal">
                        <p class="l-eyebrow">Developer tooling</p>

                        <h1 id="intro-heading" class="l-intro__headline">
                            Your errors already<br>
                            contain the answer.
                        </h1>

                        <p class="l-intro__sub">
                            ArrowLens reads the noise in error messages and documentation
                            and surfaces what matters — the problem, the likely cause,
                            a concrete fix, and the steps to verify it's gone.
                        </p>

                        <div class="l-intro__actions">
                            <router-link :to="primaryCTA" class="l-btn l-btn--primary">
                                {{ primaryCTALabel }}
                                <svg aria-hidden="true" class="l-btn__arrow" width="16" height="16" viewBox="0 0 16 16" fill="none">
                                    <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                                </svg>
                            </router-link>
                            <a href="#error-lens" class="l-btn l-btn--ghost">See how it works</a>
                        </div>
                    </div>

                    <!-- Decorative ruled lines echoing the "lens" concept -->
                    <div class="l-intro__deco" aria-hidden="true">
                        <div class="l-intro__rule-group">
                            <span class="l-intro__rule-label">error</span>
                            <div class="l-intro__rule-track">
                                <div class="l-intro__rule l-intro__rule--full"></div>
                            </div>
                        </div>
                        <div class="l-intro__rule-group">
                            <span class="l-intro__rule-label">lens</span>
                            <div class="l-intro__rule-track">
                                <div class="l-intro__rule l-intro__rule--mid"></div>
                            </div>
                        </div>
                        <div class="l-intro__rule-group">
                            <span class="l-intro__rule-label">signal</span>
                            <div class="l-intro__rule-track">
                                <div class="l-intro__rule l-intro__rule--short"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- ── 02 THE PROBLEM ──────────────────────────────── -->
            <section class="l-section l-problem" aria-labelledby="problem-heading">
                <div class="l-inner">
                    <div class="l-section__num" aria-hidden="true">02</div>
                    <h2 id="problem-heading" class="l-section__heading l-reveal">
                        The same error. Two readings.
                    </h2>
                    <p class="l-section__sub l-reveal">
                        Raw output tells you <em>what</em> broke. ArrowLens tells you <em>why</em> — and what to do about it.
                    </p>

                    <div class="l-split l-reveal">
                        <!-- Raw terminal error -->
                        <div class="l-terminal">
                            <div class="l-terminal__bar" aria-hidden="true">
                                <span class="l-terminal__dot"></span>
                                <span class="l-terminal__dot"></span>
                                <span class="l-terminal__dot"></span>
                                <span class="l-terminal__title">terminal</span>
                            </div>
                            <pre class="l-terminal__body"><code>Traceback (most recent call last):
  File "app.py", line 47, in process_order
    total = calculate_discount(price, user.tier)
  File "pricing.py", line 23, in calculate_discount
    rate = DISCOUNT_RATES[tier]
<span class="l-terminal__err">KeyError: 'enterprise'</span>

During handling of the above exception, another
exception occurred:

  File "app.py", line 51, in process_order
    raise OrderError(f"Pricing failed: {e}")
<span class="l-terminal__err">OrderError: Pricing failed: 'enterprise'</span></code></pre>
                        </div>

                        <!-- Arrow connector -->
                        <div class="l-split__arrow" aria-hidden="true">
                            <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                                <path d="M4 16h24M20 8l8 8-8 8" stroke="var(--l-num)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </div>

                        <!-- ArrowLens output -->
                        <div class="l-result-card l-result-card--compact">
                            <div class="l-result-card__badge">ArrowLens output</div>

                            <div class="l-result-card__row">
                                <span class="l-result-card__label">Problem</span>
                                <p class="l-result-card__value">
                                    <code>calculate_discount()</code> receives a <code>tier</code>
                                    value of <code>'enterprise'</code> that is not present
                                    in <code>DISCOUNT_RATES</code>.
                                </p>
                            </div>
                            <div class="l-result-card__divider" aria-hidden="true"></div>

                            <div class="l-result-card__row">
                                <span class="l-result-card__label">Likely cause</span>
                                <p class="l-result-card__value">
                                    <code>DISCOUNT_RATES</code> was defined without an
                                    <code>'enterprise'</code> key, or the tier value was
                                    introduced after the dict was last updated.
                                </p>
                            </div>
                            <div class="l-result-card__divider" aria-hidden="true"></div>

                            <div class="l-result-card__row">
                                <span class="l-result-card__label">Suggested fix</span>
                                <p class="l-result-card__value">
                                    Add an <code>'enterprise'</code> entry to
                                    <code>DISCOUNT_RATES</code>, or use
                                    <code>.get(tier, default)</code> to handle missing tiers
                                    gracefully.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- ── 03 ERROR LENS ───────────────────────────────── -->
            <section class="l-section l-feature l-feature--alt" id="error-lens" aria-labelledby="error-lens-heading">
                <div class="l-inner">
                    <div class="l-section__num" aria-hidden="true">03</div>

                    <div class="l-feature__header l-reveal">
                        <p class="l-eyebrow">Error Lens</p>
                        <h2 id="error-lens-heading" class="l-section__heading">
                            Paste an error.<br>Get a structured analysis.
                        </h2>
                        <p class="l-section__sub">
                            Paste the error message, the relevant code,
                            and a line of context. ArrowLens returns four
                            grounded fields — no guessing, no filler.
                        </p>
                    </div>

                    <!-- Annotated result card -->
                    <div class="l-annotated l-reveal">
                        <div class="l-result-card l-result-card--full">
                            <div class="l-result-card__badge">Error Lens — analysis</div>

                            <div class="l-result-card__row l-annotated__target" data-label="What broke, stated plainly">
                                <span class="l-result-card__label">Problem</span>
                                <p class="l-result-card__value">
                                    <code>db.session.commit()</code> raises
                                    <code>IntegrityError</code> because the <code>email</code>
                                    column has a UNIQUE constraint and a duplicate value
                                    was inserted on line 88 of <code>auth/routes.py</code>.
                                </p>
                            </div>
                            <div class="l-result-card__divider" aria-hidden="true"></div>

                            <div class="l-result-card__row">
                                <span class="l-result-card__label">Likely cause</span>
                                <p class="l-result-card__value">
                                    The registration endpoint does not check whether the
                                    email already exists before inserting. The uniqueness
                                    constraint is enforced at the database level, not
                                    in the application layer.
                                </p>
                            </div>
                            <div class="l-result-card__divider" aria-hidden="true"></div>

                            <div class="l-result-card__row">
                                <span class="l-result-card__label">Suggested fix</span>
                                <p class="l-result-card__value">
                                    Before the insert, query
                                    <code>User.query.filter_by(email=email).first()</code>
                                    and return a 409 if a record is found. Wrap the
                                    commit in a try/except for <code>IntegrityError</code>
                                    as a secondary guard.
                                </p>
                            </div>
                            <div class="l-result-card__divider" aria-hidden="true"></div>

                            <div class="l-result-card__row">
                                <span class="l-result-card__label">Verification</span>
                                <ul class="l-result-card__list">
                                    <li>Attempt to register with an existing email — expect HTTP 409 with a clear error message.</li>
                                    <li>Confirm the database row count for that email remains exactly one after the attempt.</li>
                                </ul>
                            </div>
                        </div>

                        <!-- Field annotations -->
                        <div class="l-annotated__notes" aria-hidden="true">
                            <span class="l-annotated__note">Based only on supplied input</span>
                            <span class="l-annotated__note">Inferred causes are labelled</span>
                            <span class="l-annotated__note">Concrete, tied to your code</span>
                            <span class="l-annotated__note">Specific to this exact error</span>
                        </div>
                    </div>

                    <div class="l-feature__cta l-reveal">
                        <router-link :to="errorLensTarget" class="l-btn l-btn--primary">
                            Try Error Lens
                            <svg aria-hidden="true" class="l-btn__arrow" width="16" height="16" viewBox="0 0 16 16" fill="none">
                                <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </router-link>
                    </div>
                </div>
            </section>

            <!-- ── 04 DOCS LENS ────────────────────────────────── -->
            <section class="l-section l-feature" id="docs-lens" aria-labelledby="docs-lens-heading">
                <div class="l-inner">
                    <div class="l-section__num" aria-hidden="true">04</div>

                    <div class="l-feature__header l-reveal">
                        <p class="l-eyebrow">Docs Lens</p>
                        <h2 id="docs-lens-heading" class="l-section__heading">
                            Paste documentation.<br>Get the parts that matter.
                        </h2>
                        <p class="l-section__sub">
                            Drop in a chunk of technical documentation — a library
                            reference, an API spec, a migration guide. ArrowLens
                            extracts the summary, key concepts, a working example,
                            and the mistake most developers make.
                        </p>
                    </div>

                    <!-- Two-column: raw docs → structured output -->
                    <div class="l-docs-split l-reveal">
                        <div class="l-docs-split__input">
                            <div class="l-docs-split__header">
                                <span class="l-eyebrow">Documentation input</span>
                            </div>
                            <div class="l-docs-paste">
<pre><code>## useEffect

The Effect Hook lets you perform side effects in
function components. Data fetching, subscriptions,
or manually changing the DOM are all examples of
side effects. Think of useEffect as componentDidMount,
componentDidUpdate, and componentWillUnmount
combined.

By default, React runs the effects after every
render — including the first one. You can opt out
of this by passing a dependency array as a second
argument. If you pass an empty array [], the effect
runs only once (after the first render).

Cleanup: If your effect returns a function, React
will run it when the component unmounts, and also
before re-running the effect due to a dependency
change.</code></pre>
                            </div>
                        </div>

                        <!-- Arrow -->
                        <div class="l-split__arrow l-split__arrow--v" aria-hidden="true">
                            <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                                <path d="M4 16h24M20 8l8 8-8 8" stroke="var(--l-num)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </div>

                        <!-- Docs Lens output -->
                        <div class="l-result-card l-result-card--full">
                            <div class="l-result-card__badge">Docs Lens — analysis</div>

                            <div class="l-result-card__row">
                                <span class="l-result-card__label">Summary</span>
                                <p class="l-result-card__value">
                                    <code>useEffect</code> runs side effects after renders.
                                    A dependency array controls when it re-runs.
                                    Returning a function from the effect registers a cleanup
                                    that runs on unmount or before the next effect.
                                </p>
                            </div>
                            <div class="l-result-card__divider" aria-hidden="true"></div>

                            <div class="l-result-card__row">
                                <span class="l-result-card__label">Key concepts</span>
                                <ul class="l-result-card__list">
                                    <li>Effect runs after every render by default</li>
                                    <li>Empty dependency array <code>[]</code> → runs once on mount</li>
                                    <li>Cleanup function returned from effect → runs on unmount</li>
                                    <li>Dependency array controls when effect re-runs</li>
                                </ul>
                            </div>
                            <div class="l-result-card__divider" aria-hidden="true"></div>

                            <div class="l-result-card__row">
                                <span class="l-result-card__label">Example</span>
                                <p class="l-result-card__value">
                                    Pass <code>[userId]</code> as the second argument to
                                    re-fetch data whenever <code>userId</code> changes,
                                    and return a cleanup that cancels the pending request
                                    to avoid state updates on unmounted components.
                                </p>
                            </div>
                            <div class="l-result-card__divider" aria-hidden="true"></div>

                            <div class="l-result-card__row">
                                <span class="l-result-card__label">Common mistake</span>
                                <p class="l-result-card__value">
                                    Omitting a dependency from the array while still
                                    referencing it inside the effect — the effect reads
                                    a stale closure value rather than the current one.
                                </p>
                            </div>
                        </div>
                    </div>

                    <div class="l-feature__cta l-reveal">
                        <router-link :to="docsLensTarget" class="l-btn l-btn--primary">
                            Try Docs Lens
                            <svg aria-hidden="true" class="l-btn__arrow" width="16" height="16" viewBox="0 0 16 16" fill="none">
                                <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </router-link>
                    </div>
                </div>
            </section>

            <!-- ── 05 THE LENS CONCEPT ─────────────────────────── -->
            <section class="l-section l-concept" aria-labelledby="concept-heading">
                <div class="l-inner">
                    <div class="l-section__num" aria-hidden="true">05</div>

                    <div class="l-concept__body l-reveal">
                        <h2 id="concept-heading" class="l-concept__headline">
                            A lens doesn't change what you see.<br>
                            It changes <em>how clearly</em> you see it.
                        </h2>
                        <p class="l-concept__copy">
                            Errors and documentation aren't broken. They contain
                            the information you need. ArrowLens extracts the signal —
                            the specific field or clause that answers your question —
                            so you spend less time parsing and more time building.
                        </p>
                    </div>

                    <!-- Inline SVG diagram: noise → lens → signal -->
                    <!-- Decorative visual elements are aria-hidden; the "signal" field names are exposed as text -->
                    <div class="l-concept__diagram l-reveal" aria-hidden="true">
                        <div class="l-concept__stage">
                            <div class="l-concept__stage-label">noise</div>
                            <div class="l-concept__noise">
                                <span class="l-noise__line l-noise__line--lg"></span>
                                <span class="l-noise__line l-noise__line--sm"></span>
                                <span class="l-noise__line l-noise__line--md"></span>
                                <span class="l-noise__line l-noise__line--sm"></span>
                                <span class="l-noise__line l-noise__line--lg"></span>
                                <span class="l-noise__line l-noise__line--xs"></span>
                                <span class="l-noise__line l-noise__line--md"></span>
                            </div>
                        </div>

                        <div class="l-concept__flow-arrow" aria-hidden="true">
                            <svg width="40" height="16" viewBox="0 0 40 16" fill="none">
                                <path d="M0 8h36M29 2l7 6-7 6" stroke="var(--l-num)" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </div>

                        <!-- Lens -->
                        <div class="l-concept__lens" aria-hidden="true">
                            <svg class="l-concept__lens-svg" width="64" height="64" viewBox="0 0 64 64" fill="none">
                                <circle cx="32" cy="32" r="28" stroke="var(--accent)" stroke-width="1.5"/>
                                <ellipse cx="32" cy="32" rx="12" ry="28" stroke="var(--accent)" stroke-width="1" opacity="0.35"/>
                                <line x1="4" y1="32" x2="60" y2="32" stroke="var(--accent)" stroke-width="0.75" opacity="0.25"/>
                            </svg>
                            <span class="l-concept__lens-label">ArrowLens</span>
                        </div>

                        <div class="l-concept__flow-arrow" aria-hidden="true">
                            <svg width="40" height="16" viewBox="0 0 40 16" fill="none">
                                <path d="M0 8h36M29 2l7 6-7 6" stroke="var(--l-num)" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </div>

                        <div class="l-concept__stage">
                            <div class="l-concept__stage-label">signal</div>
                            <div class="l-concept__signal">
                                <span class="l-signal__field">Problem</span>
                                <span class="l-signal__field">Likely cause</span>
                                <span class="l-signal__field">Suggested fix</span>
                                <span class="l-signal__field">Verification</span>
                            </div>
                        </div>
                    </div>
                    <!-- Accessible equivalent of the diagram for screen readers -->
                    <p class="l-visually-hidden">
                        The ArrowLens process: raw error or documentation noise passes through
                        the ArrowLens analysis engine and produces four structured output fields —
                        Problem, Likely cause, Suggested fix, and Verification.
                    </p>
                </div>
            </section>

            <!-- ── 06 WORKS WHERE YOU WORK ─────────────────────── -->
            <section class="l-section l-works" aria-labelledby="works-heading">
                <div class="l-inner">
                    <div class="l-section__num" aria-hidden="true">06</div>

                    <div class="l-works__header l-reveal">
                        <h2 id="works-heading" class="l-section__heading">
                            The tool, not the pitch.
                        </h2>
                        <p class="l-section__sub">
                            Both lenses share the same workspace layout —
                            input on the left, structured analysis on the right.
                            No dashboards to configure. No settings to wrestle with.
                        </p>
                    </div>

                    <div class="l-mockups l-reveal">
                        <!-- Error Lens mockup -->
                        <figure class="l-mockup">
                            <figcaption class="l-mockup__caption">
                                <span class="l-eyebrow">Error Lens</span>
                            </figcaption>
                            <div class="l-mockup__frame">
                                <div class="l-mockup__pane l-mockup__pane--input">
                                    <div class="l-mockup__field-label">Error message</div>
                                    <div class="l-mockup__textarea l-mockup__textarea--filled">KeyError: 'enterprise'</div>
                                    <div class="l-mockup__field-label">Relevant code</div>
                                    <div class="l-mockup__textarea">rate = DISCOUNT_RATES[tier]</div>
                                    <div class="l-mockup__field-label">Context</div>
                                    <div class="l-mockup__textarea l-mockup__textarea--short">Processing order checkout</div>
                                    <div class="l-mockup__btn">Analyze Error</div>
                                </div>
                                <div class="l-mockup__pane l-mockup__pane--result">
                                    <div class="l-mockup__result-section">
                                        <div class="l-mockup__result-label">Problem</div>
                                        <div class="l-mockup__result-line l-mockup__result-line--lg"></div>
                                        <div class="l-mockup__result-line l-mockup__result-line--md"></div>
                                    </div>
                                    <div class="l-mockup__result-section">
                                        <div class="l-mockup__result-label">Likely Cause</div>
                                        <div class="l-mockup__result-line l-mockup__result-line--md"></div>
                                        <div class="l-mockup__result-line l-mockup__result-line--sm"></div>
                                    </div>
                                    <div class="l-mockup__result-section">
                                        <div class="l-mockup__result-label">Suggested Fix</div>
                                        <div class="l-mockup__result-line l-mockup__result-line--lg"></div>
                                        <div class="l-mockup__result-line l-mockup__result-line--md"></div>
                                    </div>
                                    <div class="l-mockup__result-section">
                                        <div class="l-mockup__result-label">Verification</div>
                                        <div class="l-mockup__result-line l-mockup__result-line--sm"></div>
                                        <div class="l-mockup__result-line l-mockup__result-line--md"></div>
                                    </div>
                                </div>
                            </div>
                        </figure>

                        <!-- Docs Lens mockup -->
                        <figure class="l-mockup">
                            <figcaption class="l-mockup__caption">
                                <span class="l-eyebrow">Docs Lens</span>
                            </figcaption>
                            <div class="l-mockup__frame">
                                <div class="l-mockup__pane l-mockup__pane--input">
                                    <div class="l-mockup__field-label">Documentation</div>
                                    <div class="l-mockup__textarea l-mockup__textarea--tall">useEffect runs side effects after renders. Pass a dependency array as the second argument…</div>
                                    <div class="l-mockup__btn">Analyze Documentation</div>
                                </div>
                                <div class="l-mockup__pane l-mockup__pane--result">
                                    <div class="l-mockup__result-section">
                                        <div class="l-mockup__result-label">Summary</div>
                                        <div class="l-mockup__result-line l-mockup__result-line--lg"></div>
                                        <div class="l-mockup__result-line l-mockup__result-line--md"></div>
                                    </div>
                                    <div class="l-mockup__result-section">
                                        <div class="l-mockup__result-label">Key Concepts</div>
                                        <div class="l-mockup__result-line l-mockup__result-line--sm"></div>
                                        <div class="l-mockup__result-line l-mockup__result-line--md"></div>
                                        <div class="l-mockup__result-line l-mockup__result-line--sm"></div>
                                    </div>
                                    <div class="l-mockup__result-section">
                                        <div class="l-mockup__result-label">Example</div>
                                        <div class="l-mockup__result-line l-mockup__result-line--md"></div>
                                    </div>
                                    <div class="l-mockup__result-section">
                                        <div class="l-mockup__result-label">Common Mistake</div>
                                        <div class="l-mockup__result-line l-mockup__result-line--lg"></div>
                                        <div class="l-mockup__result-line l-mockup__result-line--sm"></div>
                                    </div>
                                </div>
                            </div>
                        </figure>
                    </div>
                </div>
            </section>

            <!-- ── 07 HOW WE THINK ABOUT QUALITY ──────────────── -->
            <section class="l-section l-quality" aria-labelledby="quality-heading">
                <div class="l-inner">
                    <div class="l-section__num" aria-hidden="true">07</div>

                    <h2 id="quality-heading" class="l-section__heading l-reveal">
                        How we think about quality.
                    </h2>

                    <div class="l-quality__grid l-reveal">
                        <div class="l-quality__item">
                            <div class="l-quality__marker" aria-hidden="true">—</div>
                            <div>
                                <h3 class="l-quality__title">Keyboard first</h3>
                                <p class="l-quality__body">
                                    Every action reachable by tab. Focus states visible,
                                    not an afterthought. No mouse required.
                                </p>
                            </div>
                        </div>
                        <div class="l-quality__item">
                            <div class="l-quality__marker" aria-hidden="true">—</div>
                            <div>
                                <h3 class="l-quality__title">Readable contrast</h3>
                                <p class="l-quality__body">
                                    Text and interface elements meet WCAG AA contrast
                                    ratios. Information never depends on colour alone.
                                </p>
                            </div>
                        </div>
                        <div class="l-quality__item">
                            <div class="l-quality__marker" aria-hidden="true">—</div>
                            <div>
                                <h3 class="l-quality__title">Motion that respects you</h3>
                                <p class="l-quality__body">
                                    Animations follow your system's
                                    <code>prefers-reduced-motion</code> preference.
                                    The product works without them.
                                </p>
                            </div>
                        </div>
                        <div class="l-quality__item">
                            <div class="l-quality__marker" aria-hidden="true">—</div>
                            <div>
                                <h3 class="l-quality__title">Clear information hierarchy</h3>
                                <p class="l-quality__body">
                                    Every analysis field is labelled. Output is structured,
                                    not prose — so you scan, not read.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- ── 08 FINAL CTA ────────────────────────────────── -->
            <section class="l-section l-cta" aria-labelledby="cta-heading">
                <div class="l-inner">
                    <div class="l-cta__body l-reveal">
                        <h2 id="cta-heading" class="l-cta__headline">
                            Start reading your errors differently.
                        </h2>
                        <p class="l-cta__sub">
                            Free to use. No configuration required.
                        </p>
                        <div class="l-cta__actions">
                            <router-link :to="primaryCTA" class="l-btn l-btn--primary l-btn--lg">
                                {{ authed ? 'Go to dashboard' : 'Create account' }}
                                <svg aria-hidden="true" class="l-btn__arrow" width="16" height="16" viewBox="0 0 16 16" fill="none">
                                    <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                                </svg>
                            </router-link>
                            <router-link v-if="!authed" to="/login" class="l-btn l-btn--outline l-btn--lg">
                                Sign in
                            </router-link>
                        </div>
                    </div>
                </div>
            </section>

        </main>

        <!-- ── FOOTER ──────────────────────────────────────────── -->
        <footer class="l-footer" role="contentinfo">
            <div class="l-inner l-footer__inner">
                <a href="/" class="l-footer__brand al-brand-lockup al-brand-lockup--footer" aria-label="ArrowLens home">
                    <img :src="logo" alt="" aria-hidden="true" class="al-brand-lockup__mark" />
                    <span class="al-brand-lockup__wordmark">ArrowLens</span>
                </a>
                <p class="l-footer__copy">
                    Made for developers.
                </p>
            </div>
        </footer>

    </div>
</template>

<style scoped>
/* ── Base layout ─────────────────────────────────────── */

.landing {
    width: 100%;
    min-height: 100svh;
    background: var(--bg);
    color: var(--text);
    font-family: var(--sans);
    text-align: left;
}

.l-inner {
    max-width: var(--l-max);
    margin: 0 auto;
    padding: 0 32px;
    position: relative;
}

/* ── Sections ────────────────────────────────────────── */

.l-section {
    padding: 96px 0;
    border-top: 1px solid var(--l-rule);
}

.l-section:first-of-type,
.l-intro {
    border-top: none;
    padding-top: 80px;
}

.l-feature--alt {
    background: var(--l-surface);
}

/* ── Section numbering ───────────────────────────────── */

.l-section__num {
    font-family: var(--mono);
    font-size: calc((11px) * var(--accessibility-text-scale, 1));
    color: var(--l-num);
    letter-spacing: 0.08em;
    margin-bottom: 20px;
    display: block;
}

/* ── Typography helpers ──────────────────────────────── */

.l-eyebrow {
    font-size: calc((11px) * var(--accessibility-text-scale, 1));
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--l-tag);
    margin: 0 0 12px;
    display: block;
}

.l-section__heading {
    font-family: var(--heading);
    font-size: calc((clamp(28px, 4vw, 44px)) * var(--accessibility-text-scale, 1));
    font-weight: 400;
    letter-spacing: -0.02em;
    line-height: 1.15;
    color: var(--text-h);
    margin: 0 0 16px;
}

.l-section__sub {
    font-size: calc((17px) * var(--accessibility-text-scale, 1));
    line-height: 1.65;
    color: var(--text);
    max-width: 560px;
    margin: 0;
}

/* ── Entrance animation ──────────────────────────────── */

.l-reveal {
    opacity: 0;
    transform: translateY(18px);
    transition: opacity 0.55s ease, transform 0.55s ease;
}

.l-reveal--visible {
    opacity: 1;
    transform: translateY(0);
}

/* ── Buttons ─────────────────────────────────────────── */

.l-btn {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    font-family: var(--sans);
    font-size: calc((14px) * var(--accessibility-text-scale, 1));
    font-weight: 500;
    text-decoration: none;
    border-radius: 6px;
    padding: 9px 16px;
    border: none;
    cursor: pointer;
    transition: background 0.18s, gap 0.18s, border-color 0.18s, color 0.18s;
    white-space: nowrap;
}

.l-btn--lg {
    font-size: calc((15px) * var(--accessibility-text-scale, 1));
    padding: 11px 20px;
}

.l-btn--primary {
    background: var(--text-h);
    color: var(--bg);
}

.l-btn--primary:hover .l-btn__arrow {
    transform: translateX(3px);
}

.l-btn--primary:hover {
    background: var(--accent-hover);
}

:root[data-theme="dark"] .l-btn--primary:hover {
    background: #1e1a2e;
}

.l-btn__arrow {
    transition: transform 0.18s ease;
    flex-shrink: 0;
}

.l-btn--ghost {
    color: var(--text);
    background: transparent;
    border: 1px solid var(--l-rule);
}

.l-btn--ghost:hover {
    border-color: var(--border);
    color: var(--text-h);
}

.l-btn--outline {
    color: var(--text-h);
    background: transparent;
    border: 1px solid var(--border);
}

.l-btn--outline:hover {
    background: var(--l-surface);
}

.l-btn:focus-visible {
    outline: 2px solid var(--accent);
    outline-offset: 3px;
}

/* ── 01 Intro ────────────────────────────────────────── */

.l-intro__body {
    max-width: 680px;
}

.l-intro__headline {
    font-family: var(--heading);
    font-size: calc((clamp(38px, 6vw, 72px)) * var(--accessibility-text-scale, 1));
    font-weight: 400;
    letter-spacing: -0.03em;
    line-height: 1.05;
    color: var(--text-h);
    margin: 8px 0 24px;
}

.l-intro__sub {
    font-size: calc((18px) * var(--accessibility-text-scale, 1));
    line-height: 1.65;
    color: var(--text);
    max-width: 520px;
    margin-bottom: 36px;
}

.l-intro__actions {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
}

/* Decorative ruled lines */
.l-intro__deco {
    position: absolute;
    right: 32px;
    top: 0;
    bottom: 0;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 20px;
    width: 200px;
}

.l-intro__rule-group {
    display: flex;
    align-items: center;
    gap: 12px;
}

.l-intro__rule-label {
    font-family: var(--mono);
    font-size: calc((10px) * var(--accessibility-text-scale, 1));
    color: var(--l-num);
    width: 44px;
    text-align: right;
    flex-shrink: 0;
}

.l-intro__rule-track {
    flex: 1;
    height: 1px;
    background: var(--l-rule);
    position: relative;
    overflow: hidden;
}

.l-intro__rule {
    position: absolute;
    left: 0;
    top: 0;
    height: 1px;
    background: var(--l-num);
    opacity: 0.6;
}

.l-intro__rule--full  { width: 100%; }
.l-intro__rule--mid   { width: 52%; }
.l-intro__rule--short { width: 28%; }

/* ── 02 Problem split layout ─────────────────────────── */

.l-split {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    gap: 24px;
    align-items: center;
    margin-top: 48px;
}

.l-split__arrow {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0 8px;
    opacity: 0.6;
}

/* Terminal block */
.l-terminal {
    background: var(--l-terminal-bg);
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.06);
}

.l-terminal__bar {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 10px 14px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}

.l-terminal__dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: rgba(255,255,255,0.12);
    display: block;
}

.l-terminal__title {
    font-family: var(--mono);
    font-size: calc((11px) * var(--accessibility-text-scale, 1));
    color: var(--l-terminal-dim);
    margin-left: 4px;
}

.l-terminal__body {
    margin: 0;
    padding: 20px;
    font-family: var(--mono);
    font-size: calc((12.5px) * var(--accessibility-text-scale, 1));
    line-height: 1.7;
    color: #abb2bf;
    overflow-x: auto;
    white-space: pre;
}

.l-terminal__err {
    color: var(--l-terminal-red);
}

/* Result card */
.l-result-card {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
}

.l-result-card--compact .l-result-card__row {
    padding: 14px 18px;
}

.l-result-card--full .l-result-card__row {
    padding: 18px 22px;
}

.l-result-card__badge {
    font-family: var(--mono);
    font-size: calc((10px) * var(--accessibility-text-scale, 1));
    color: var(--l-tag);
    padding: 8px 18px;
    border-bottom: 1px solid var(--l-rule);
    background: var(--l-surface);
    letter-spacing: 0.04em;
}

.l-result-card__label {
    display: block;
    font-size: calc((11px) * var(--accessibility-text-scale, 1));
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    color: var(--l-tag);
    margin-bottom: 7px;
}

.l-result-card__value {
    margin: 0;
    font-size: calc((14px) * var(--accessibility-text-scale, 1));
    line-height: 1.6;
    color: var(--text-h);
}

.l-result-card__value code {
    font-size: calc((12.5px) * var(--accessibility-text-scale, 1));
    padding: 1px 5px;
    background: var(--code-bg);
    border-radius: 3px;
    color: var(--text-h);
}

.l-result-card__list {
    margin: 0;
    padding-left: 18px;
    font-size: calc((14px) * var(--accessibility-text-scale, 1));
    line-height: 1.65;
    color: var(--text-h);
}

.l-result-card__list li {
    margin-bottom: 5px;
}

.l-result-card__list code {
    font-size: calc((12.5px) * var(--accessibility-text-scale, 1));
    padding: 1px 5px;
    background: var(--code-bg);
    border-radius: 3px;
}

.l-result-card__divider {
    height: 1px;
    background: var(--l-rule);
    margin: 0;
}

/* ── 03 Error Lens annotated ─────────────────────────── */

.l-feature__header {
    max-width: 600px;
    margin-bottom: 48px;
}

.l-feature__cta {
    margin-top: 36px;
}

.l-annotated {
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 0 32px;
    align-items: start;
}

.l-annotated__notes {
    display: flex;
    flex-direction: column;
    gap: 0;
    padding-top: 52px; /* align with first row after badge */
}

.l-annotated__note {
    font-size: calc((11px) * var(--accessibility-text-scale, 1));
    color: var(--l-tag);
    font-style: italic;
    padding: 26px 0;
    border-bottom: 1px solid var(--l-rule);
    line-height: 1.4;
    max-width: 160px;
}

.l-annotated__note:last-child {
    border-bottom: none;
}

/* ── 04 Docs Lens split ──────────────────────────────── */

.l-docs-split {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    gap: 24px;
    align-items: start;
    margin-top: 48px;
}

.l-split__arrow--v {
    margin-top: 120px;
}

.l-docs-split__header {
    margin-bottom: 8px;
}

.l-docs-paste {
    background: var(--l-surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 18px 20px;
    overflow: auto;
}

.l-docs-paste pre {
    margin: 0;
    font-family: var(--mono);
    font-size: calc((12px) * var(--accessibility-text-scale, 1));
    line-height: 1.7;
    color: var(--text);
    white-space: pre-wrap;
    word-break: break-word;
}

.l-docs-paste code {
    background: none;
    padding: 0;
    font-size: inherit;
}

/* ── 05 Lens concept ─────────────────────────────────── */

.l-concept__body {
    max-width: 680px;
    margin-bottom: 64px;
}

.l-concept__headline {
    font-family: var(--heading);
    font-size: calc((clamp(24px, 3.5vw, 40px)) * var(--accessibility-text-scale, 1));
    font-weight: 400;
    letter-spacing: -0.02em;
    line-height: 1.2;
    color: var(--text-h);
    margin: 0 0 20px;
}

.l-concept__headline em {
    font-style: italic;
    color: var(--accent);
}

.l-concept__copy {
    font-size: calc((16px) * var(--accessibility-text-scale, 1));
    line-height: 1.7;
    color: var(--text);
    max-width: 560px;
}

.l-concept__diagram {
    display: flex;
    align-items: center;
    gap: 24px;
    flex-wrap: wrap;
}

.l-concept__stage {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
    min-width: 140px;
}

.l-concept__stage-label {
    font-family: var(--mono);
    font-size: calc((11px) * var(--accessibility-text-scale, 1));
    color: var(--l-num);
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

.l-concept__noise {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.l-noise__line {
    display: block;
    height: 3px;
    border-radius: 2px;
    background: var(--l-rule);
}

.l-noise__line--xs  { width: 40px; }
.l-noise__line--sm  { width: 70px; }
.l-noise__line--md  { width: 100px; }
.l-noise__line--lg  { width: 140px; }

.l-concept__flow-arrow {
    opacity: 0.5;
    flex-shrink: 0;
}

.l-concept__lens {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    flex-shrink: 0;
}

.l-concept__lens-label {
    font-family: var(--mono);
    font-size: calc((10px) * var(--accessibility-text-scale, 1));
    color: var(--accent);
    letter-spacing: 0.06em;
}

.l-concept__signal {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.l-signal__field {
    font-size: calc((12px) * var(--accessibility-text-scale, 1));
    color: var(--text-h);
    background: var(--l-surface);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 4px 10px;
    font-family: var(--mono);
    display: block;
    white-space: nowrap;
}

/* ── 06 Works — mockups ──────────────────────────────── */

.l-works__header {
    max-width: 560px;
    margin-bottom: 56px;
}

.l-mockups {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 32px;
}

.l-mockup {
    margin: 0;
}

.l-mockup__caption {
    margin-bottom: 12px;
}

.l-mockup__frame {
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
    display: grid;
    grid-template-columns: 1fr 1fr;
    background: var(--bg);
}

.l-mockup__pane {
    padding: 16px;
}

.l-mockup__pane--input {
    border-right: 1px solid var(--l-rule);
    display: flex;
    flex-direction: column;
    gap: 8px;
    background: var(--bg);
}

.l-mockup__pane--result {
    background: var(--l-surface);
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.l-mockup__field-label {
    font-size: calc((10px) * var(--accessibility-text-scale, 1));
    font-weight: 700;
    color: var(--l-tag);
    text-transform: uppercase;
    letter-spacing: 0.07em;
}

.l-mockup__textarea {
    font-family: var(--mono);
    font-size: calc((10px) * var(--accessibility-text-scale, 1));
    color: var(--text);
    background: var(--l-surface);
    border: 1px solid var(--l-rule);
    border-radius: 5px;
    padding: 8px;
    min-height: 36px;
    line-height: 1.5;
}

.l-mockup__textarea--filled {
    color: var(--text-h);
    border-color: var(--border);
}

.l-mockup__textarea--short {
    min-height: 24px;
}

.l-mockup__textarea--tall {
    min-height: 120px;
    flex: 1;
}

.l-mockup__btn {
    font-size: calc((10px) * var(--accessibility-text-scale, 1));
    font-weight: 600;
    color: var(--bg);
    background: var(--text-h);
    border-radius: 5px;
    padding: 7px 10px;
    text-align: center;
    margin-top: 4px;
}

.l-mockup__result-section {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.l-mockup__result-label {
    font-size: calc((9px) * var(--accessibility-text-scale, 1));
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--l-tag);
}

.l-mockup__result-line {
    height: 3px;
    border-radius: 2px;
    background: var(--l-rule);
}

.l-mockup__result-line--sm  { width: 55%; }
.l-mockup__result-line--md  { width: 75%; }
.l-mockup__result-line--lg  { width: 90%; }

/* ── 07 Quality grid ─────────────────────────────────── */

.l-quality__grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0;
    margin-top: 40px;
}

.l-quality__item {
    display: flex;
    gap: 16px;
    padding: 32px 0;
    border-bottom: 1px solid var(--l-rule);
}

.l-quality__item:nth-child(odd) {
    padding-right: 48px;
    border-right: 1px solid var(--l-rule);
}

.l-quality__item:nth-child(even) {
    padding-left: 48px;
}

.l-quality__item:nth-last-child(-n+2) {
    border-bottom: none;
}

.l-quality__marker {
    font-family: var(--mono);
    font-size: calc((18px) * var(--accessibility-text-scale, 1));
    color: var(--l-num);
    flex-shrink: 0;
    margin-top: 2px;
    line-height: 1;
}

.l-quality__title {
    font-size: calc((15px) * var(--accessibility-text-scale, 1));
    font-weight: 600;
    color: var(--text-h);
    margin: 0 0 8px;
    letter-spacing: -0.01em;
}

.l-quality__body {
    font-size: calc((14px) * var(--accessibility-text-scale, 1));
    line-height: 1.65;
    color: var(--text);
    margin: 0;
}

.l-quality__body code {
    font-size: calc((12.5px) * var(--accessibility-text-scale, 1));
    padding: 1px 5px;
    background: var(--code-bg);
    border-radius: 3px;
}

/* ── 08 Final CTA ────────────────────────────────────── */

.l-cta {
    background: var(--l-surface);
}

.l-cta__body {
    max-width: 560px;
}

.l-cta__headline {
    font-family: var(--heading);
    font-size: calc((clamp(26px, 4vw, 44px)) * var(--accessibility-text-scale, 1));
    font-weight: 400;
    letter-spacing: -0.02em;
    line-height: 1.15;
    color: var(--text-h);
    margin: 0 0 12px;
}

.l-cta__sub {
    font-size: calc((16px) * var(--accessibility-text-scale, 1));
    color: var(--text);
    margin-bottom: 36px;
}

.l-cta__actions {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
}

/* ── Footer ──────────────────────────────────────────── */

.l-footer {
    border-top: 1px solid var(--l-rule);
    padding: 28px 0;
}

.l-footer__inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
}

.l-footer__brand {
    display: flex;
    align-items: center;
    gap: 8px;
    text-decoration: none;
    font-size: calc((13px) * var(--accessibility-text-scale, 1));
    font-weight: 600;
    color: var(--text-h);
}

.l-footer__brand:focus-visible {
    outline: 2px solid var(--accent);
    outline-offset: 2px;
    border-radius: 3px;
}

.l-footer__copy {
    font-size: calc((12px) * var(--accessibility-text-scale, 1));
    color: var(--l-tag);
    margin: 0;
}

/* ── Responsive ──────────────────────────────────────── */

@media (max-width: 900px) {
    .l-inner {
        padding: 0 24px;
    }

    .l-section {
        padding: 64px 0;
    }

    .l-split {
        grid-template-columns: 1fr;
        gap: 16px;
    }

    .l-split__arrow {
        transform: rotate(90deg);
        margin: 0 auto;
    }

    .l-docs-split {
        grid-template-columns: 1fr;
        gap: 16px;
    }

    .l-split__arrow--v {
        margin: 0 auto;
        transform: rotate(90deg);
    }

    .l-annotated {
        grid-template-columns: 1fr;
    }

    .l-annotated__notes {
        display: none;
    }

    .l-mockups {
        grid-template-columns: 1fr;
    }

    .l-quality__grid {
        grid-template-columns: 1fr;
    }

    .l-quality__item:nth-child(odd) {
        padding-right: 0;
        border-right: none;
    }

    .l-quality__item:nth-child(even) {
        padding-left: 0;
    }

    .l-quality__item:nth-last-child(-n+2) {
        border-bottom: 1px solid var(--l-rule);
    }

    .l-quality__item:last-child {
        border-bottom: none;
    }

    .l-intro__deco {
        display: none;
    }

    .l-concept__diagram {
        gap: 16px;
    }
}

@media (max-width: 600px) {
    .l-inner {
        padding: 0 20px;
    }

    .l-section {
        padding: 48px 0;
    }

    .l-intro__headline {
        font-size: calc((36px) * var(--accessibility-text-scale, 1));
    }

    .l-intro__sub {
        font-size: calc((16px) * var(--accessibility-text-scale, 1));
    }

    .l-intro__actions {
        flex-direction: column;
        align-items: flex-start;
    }

    .l-concept__diagram {
        flex-direction: column;
        align-items: flex-start;
    }

    .l-concept__flow-arrow {
        transform: rotate(90deg);
        margin-left: 64px;
    }

    .l-cta__actions {
        flex-direction: column;
        align-items: flex-start;
    }
}

/* ── Visually hidden (screen-reader only) ────────────── */

.l-visually-hidden {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}
</style>
