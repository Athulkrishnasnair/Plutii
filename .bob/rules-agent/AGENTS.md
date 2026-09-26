# AGENTS.md — Agent (coding) mode

This file provides guidance to agents when working with code in this repository.

## Critical: `google-genai` import is deferred

Both `ai_service.py` and `docs_service.py` import `google.genai` **inside** the function body, not at the module top. Maintain this pattern when adding new service functions — it avoids import-time failures when the package is absent.

## Adding a new AI feature

Follow this three-file pattern (see ErrorLens as reference):
1. `backend/app/services/<feature>_service.py` — `_build_prompt`, `_extract_json`, `_validate_result`, `analyze_<feature>()`. Always raise `RuntimeError` (never let raw exceptions escape to routes).
2. `backend/app/<feature>/routes.py` — Blueprint with `url_prefix="/api/<feature>"`. Auth guard (`session.get("user_id")`) must be the first check in every route.
3. Register blueprint in `backend/app/__init__.py`.
4. Add `export function analyze<Feature>()` to `frontend/src/services/api.js`.
5. Add route in `frontend/src/router/index.js` using lazy import.

## Session auth guard — copy this exact pattern

```python
user_id = session.get("user_id")
if not user_id:
    return jsonify({"error": "Not authenticated"}), 401
```

Every protected route must open with this block before touching request data.

## `docs_service.py` default model mismatch

`_DEFAULT_MODEL = "gemini-3.5-flash-lite"` in `docs_service.py` is different from `"gemini-2.0-flash"` in `ai_service.py`. When both services are called and `GEMINI_MODEL` env var is not set, they use different models. Set `GEMINI_MODEL` explicitly to unify them.

## DB setup

`db.create_all()` runs on every app startup inside `app/__init__.py`. There is no migration system — schema changes require dropping and recreating the SQLite file at `backend/instance/plutii.db`.

## No test framework

There are no tests. When adding tests, choose pytest (already compatible with the venv structure) and place test files under `backend/tests/`.
