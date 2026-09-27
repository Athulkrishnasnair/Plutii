import { createHighlighter } from 'shiki';

let highlighterPromise = null;

// Map file extensions and common aliases to Shiki supported language IDs
const LANG_MAP = {
    vue: 'vue',
    js: 'javascript',
    javascript: 'javascript',
    mjs: 'javascript',
    cjs: 'javascript',
    ts: 'typescript',
    typescript: 'typescript',
    jsx: 'jsx',
    tsx: 'tsx',
    py: 'python',
    python: 'python',
    html: 'html',
    css: 'css',
    scss: 'css',
    json: 'json',
    sql: 'sql',
    sh: 'bash',
    bash: 'bash',
    zsh: 'bash',
    shell: 'bash',
    md: 'markdown',
    markdown: 'markdown',
    yaml: 'yaml',
    yml: 'yaml',
    xml: 'xml',
    txt: 'text',
    text: 'text'
};

const SUPPORTED_LANGS = [
    'vue',
    'javascript',
    'typescript',
    'jsx',
    'tsx',
    'python',
    'html',
    'css',
    'json',
    'sql',
    'bash',
    'markdown'
];

export function normalizeLanguage(langOrExt) {
    if (!langOrExt) return 'text';
    const clean = langOrExt.toString().trim().toLowerCase().replace(/^\./, '');
    return LANG_MAP[clean] || 'text';
}

export function detectLanguageFromPath(filePath) {
    if (!filePath) return 'text';
    const match = filePath.match(/\.([a-zA-Z0-9]+)$/);
    if (match && match[1]) {
        return normalizeLanguage(match[1]);
    }
    return 'text';
}

export async function getHighlighterInstance() {
    if (!highlighterPromise) {
        highlighterPromise = createHighlighter({
            themes: ['github-dark', 'github-light'],
            langs: SUPPORTED_LANGS
        }).catch((err) => {
            console.warn('Failed to initialize Shiki highlighter, falling back to plaintext:', err);
            highlighterPromise = null;
            return null;
        });
    }
    return highlighterPromise;
}

/**
 * Highlight code snippet asynchronously using Shiki.
 * Returns raw HTML string.
 */
export async function highlightCode(code, lang = 'text', theme = 'github-dark') {
    if (!code) return '';
    const normalizedLang = normalizeLanguage(lang);

    try {
        const hl = await getHighlighterInstance();
        if (hl && (SUPPORTED_LANGS.includes(normalizedLang) || normalizedLang === 'text')) {
            return hl.codeToHtml(code, {
                lang: normalizedLang === 'text' ? 'text' : normalizedLang,
                theme: theme
            });
        }
    } catch (err) {
        console.warn('Shiki highlighting error:', err);
    }

    // Graceful fallback to escaped HTML
    return `<pre class="shiki-fallback"><code>${escapeHtml(code)}</code></pre>`;
}

/**
 * Tokenize code line-by-line for interactive code viewers (e.g. with line numbers & selection).
 * Returns Array of lines, where each line is an Array of tokens { content, color, fontStyle }.
 */
export async function tokenizeCode(code, lang = 'text', theme = 'github-dark') {
    if (!code) return [];
    const normalizedLang = normalizeLanguage(lang);

    try {
        const hl = await getHighlighterInstance();
        if (hl) {
            const res = hl.codeToTokens(code, {
                lang: normalizedLang === 'text' ? 'text' : normalizedLang,
                theme: theme
            });
            if (res && res.tokens) {
                return res.tokens;
            }
        }
    } catch (err) {
        console.warn('Shiki tokenization failed:', err);
    }

    // Graceful fallback: one token per line
    return (code || '').split('\n').map(line => [{ content: line || ' ', color: 'inherit' }]);
}

export function escapeHtml(str) {
    if (!str) return '';
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}
