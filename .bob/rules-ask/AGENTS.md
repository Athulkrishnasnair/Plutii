# AGENTS.md — Ask mode

This file provides guidance to agents when working with code in this repository.

## App identity

README calls the project "Plutii"; the workspace folder and `.env.example` call it "ArrowLens". The deployed name visible in the UI is ArrowLens. README is partially outdated.

## Two separate fetch wrappers

`frontend/src/services/api.js` and `frontend/src/services/auth.js` are **both** thin fetch wrappers pointing at `http://localhost:5000/api` — they are not shared utilities. `api.js` handles notes + AI endpoints; `auth.js` handles auth. Both require `credentials: "include"`.

## AI features live at dedicated routes

- ErrorLens → `POST /api/analysis/error` — returns `{ problem, cause, fix, verification[] }`
- DocsLens → `POST /api/docs/analyze` — returns `{ summary, key_concepts[], example, common_mistake }`

Both are auth-gated (session cookie required).

## CORS is hard-coded

`flask_cors` is configured in `app/__init__.py` to allow only `http://localhost:5173`. Any other origin (including `https://` or a different port) will be blocked. This is not in a config file — it must be changed in code.

## No environment variable for the DB

The SQLite URI `sqlite:///plutii.db` is hard-coded in `app/__init__.py`. There is no env var override.
