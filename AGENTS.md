# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Project Overview

ArrowLens (README calls it "Plutii") is a full-stack developer-tools app: Vue 3 + Vite frontend, Flask + SQLAlchemy backend, using Google Gemini for AI analysis features (ErrorLens, DocsLens).

## Commands

### Backend
```bash
# From backend/ directory — activate venv first
source .venv/bin/activate           # Linux/macOS
.venv\Scripts\Activate.ps1          # Windows PowerShell

python run.py                        # Dev server on http://localhost:5000
```

### Frontend
```bash
# From frontend/ directory
npm run dev     # Dev server on http://localhost:5173
npm run build
```

No test framework is set up; there are no test files in the project.

## Environment Variables (backend only)

Copy `backend/.env.example` → `backend/.env` before running.

| Variable | Required | Default |
|---|---|---|
| `GEMINI_API_KEY` | Yes | — |
| `GEMINI_MODEL` | No | `gemini-2.0-flash` |

**Note:** `docs_service.py` hardcodes `_DEFAULT_MODEL = "gemini-3.5-flash-lite"` as its own override, ignoring `GEMINI_MODEL` unless the env var is set — different default from `ai_service.py`.

## Architecture

- All API routes are prefixed `/api/*` and registered as Blueprints in [`backend/app/__init__.py`](backend/app/__init__.py)
- Auth is **Flask session-based** (cookie). CORS is locked to `http://localhost:5173` with `supports_credentials=True`
- Frontend uses `credentials: "include"` on every fetch — required for session cookies to work cross-origin
- SQLite DB file is `backend/instance/plutii.db` (auto-created on first run via `db.create_all()`)
- `SECRET_KEY` is hardcoded as `"dev-secret-key"` — must be changed for any real deployment

## Backend Code Patterns

- **Service layer** (`app/services/`) handles all Gemini calls; routes only validate input and call services
- **`google-genai` is imported inside the function body** (`import google.genai as genai`) in both service files — not at module top
- Gemini errors are caught broadly (`except Exception`) in services and re-raised as `RuntimeError` with safe user-facing messages; routes return `503` for these
- JSON from Gemini is stripped of markdown fences via `_extract_json()` before parsing — Gemini sometimes wraps output in ` ```json ``` `
- Route auth guard pattern: always check `session.get("user_id")` first, return `401` if missing, before any other logic
- `db.session.get(Model, id)` is used for PK lookups (SQLAlchemy 2.x style), not `Model.query.get(id)`

## Frontend Code Patterns

- Two separate API service files: [`frontend/src/services/api.js`](frontend/src/services/api.js) (notes + AI) and [`frontend/src/services/auth.js`](frontend/src/services/auth.js) (auth) — both wrap `fetch` with `credentials: "include"`
- Router uses lazy imports (`() => import(...)`) for all views — no eager loading
- No state management library (no Pinia/Vuex); auth state is checked via `/api/auth/me` requests

## Naming Conventions

- Backend blueprints: `<feature>_bp`, url prefix `/api/<feature>`
- Service functions: `analyze_<thing>()` in `app/services/<thing>_service.py`
- Frontend views: `<Name>View.vue` in `src/views/`; components in `src/components/`
