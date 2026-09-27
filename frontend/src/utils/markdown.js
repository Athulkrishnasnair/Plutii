import MarkdownIt from 'markdown-it';
import { getHighlighterInstance, normalizeLanguage, escapeHtml } from '../services/highlighter';

let syncHighlighter = null;

// Initialize the highlighter eagerly in background
getHighlighterInstance().then(hl => {
    syncHighlighter = hl;
});

const md = new MarkdownIt({
    html: false,
    xhtmlOut: false,
    breaks: true,
    langPrefix: 'language-',
    linkify: true,
    typographer: false,
    highlight: function (str, lang) {
        const normalized = normalizeLanguage(lang);
        if (syncHighlighter) {
            try {
                return syncHighlighter.codeToHtml(str, {
                    lang: normalized === 'text' ? 'text' : normalized,
                    theme: 'github-dark'
                });
            } catch (err) {
                console.warn('Highlight failed in markdown-it:', err);
            }
        }
        return `<pre class="shiki-fallback"><code class="language-${normalized}">${escapeHtml(str)}</code></pre>`;
    }
});

// Custom renderer rule for links to make them open in new tab and safe
const defaultRender = md.renderer.rules.link_open || function (tokens, idx, options, env, self) {
    return self.renderToken(tokens, idx, options);
};

md.renderer.rules.link_open = function (tokens, idx, options, env, self) {
    const aIndex = tokens[idx].attrIndex('target');
    if (aIndex < 0) {
        tokens[idx].attrPush(['target', '_blank']);
    } else {
        tokens[idx].attrs[aIndex][1] = '_blank';
    }

    const relIndex = tokens[idx].attrIndex('rel');
    if (relIndex < 0) {
        tokens[idx].attrPush(['rel', 'noopener noreferrer']);
    } else {
        tokens[idx].attrs[relIndex][1] = 'noopener noreferrer';
    }

    return defaultRender(tokens, idx, options, env, self);
};

/**
 * Render a markdown string to sanitized HTML with highlighted code blocks.
 */
export function renderMarkdown(content) {
    if (!content || typeof content !== 'string') return '';
    return md.render(content.trim());
}

/**
 * Render inline markdown (for short labels or single sentences without wrapping <p>).
 */
export function renderInlineMarkdown(content) {
    if (!content || typeof content !== 'string') return '';
    return md.renderInline(content.trim());
}

export default md;
