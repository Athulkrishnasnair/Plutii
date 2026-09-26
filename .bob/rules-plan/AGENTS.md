# AGENTS.md — Plan mode

This file provides guidance to agents when working with code in this repository.

## Architectural constraints

- **No migration system.** Schema changes to `Note` or `User` models in `models.py` require dropping `backend/instance/plutii.db` and recreating. Planning any model change must account for data loss.
- **Session auth is stateful.** Flask sessions are server-side (cookie-based). There is no JWT or token mechanism. Any plan requiring stateless auth needs a full auth layer replacement.
- **CORS hard-locked to localhost.** Deploying frontend to any non-`localhost:5173` origin requires changing code in `app/__init__.py`, not config.
- **Two AI services are structurally identical but independent.** `ai_service.py` and `docs_service.py` share no code despite near-identical structure (`_build_prompt`, `_extract_json`, `_validate_result`). Refactoring into a shared base is feasible but currently they are copy-pasted with different prompt shapes and default models.
- **Gemini API key is global.** Both service files read the same `GEMINI_API_KEY` env var. There is no per-feature key or quota separation.
- **Frontend has no state management.** Auth state is re-fetched via `/api/auth/me` on demand. Any plan requiring reactive global state needs Pinia or equivalent added.
- **`SECRET_KEY` is a plaintext dev string** (`"dev-secret-key"`) in `app/__init__.py`. Any production plan must externalise this via env var.

## Extension points (clear seams)

- New AI lens: add a service file + blueprint + register in `__init__.py` + frontend service function + router entry — all independent, no shared state to coordinate.
- New DB models: add to `models.py`, import in `__init__.py` before `db.create_all()`.
