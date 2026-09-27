import os
from flask import Flask
from dotenv import load_dotenv
from .extensions import db
from flask_cors import CORS


load_dotenv()

def create_app():
    app = Flask(__name__)

    # ── SECRET KEY ────────────────────────────────────────────────
    # Must be set via the SECRET_KEY environment variable.
    # A missing key at startup is a configuration error — fail fast.
    secret_key = os.environ.get("SECRET_KEY")
    if not secret_key:
        raise RuntimeError(
            "SECRET_KEY environment variable is not set. "
            "Add it to backend/.env before running."
        )
    app.config["SECRET_KEY"] = secret_key

    # ── CORS ──────────────────────────────────────────────────────
    # ALLOWED_ORIGINS: comma-separated list of allowed frontend origins.
    # Defaults to localhost dev server; set in production to the real URL.
    raw_origins = os.environ.get("ALLOWED_ORIGINS") or "http://localhost:5173"
    allowed_origins = [o.strip() for o in raw_origins.split(",") if o.strip()]
    if not allowed_origins or "*" in allowed_origins:
        raise RuntimeError(
            "ALLOWED_ORIGINS must contain explicit origins when credentialed CORS is enabled."
        )
    CORS(app,
         supports_credentials=True,
         origins=allowed_origins,
         )

    # ── DATABASE ──────────────────────────────────────────────────
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///plutii.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ── SESSION COOKIES ───────────────────────────────────────────
    # HttpOnly: browser JS cannot read the session cookie (always on).
    app.config["SESSION_COOKIE_HTTPONLY"] = True

    # Secure: only send the cookie over HTTPS.
    # Set COOKIE_SECURE=true in your production .env.
    # Leave unset (or set to anything else) for local HTTP dev.
    session_cookie_secure = (
        os.environ.get("COOKIE_SECURE", "false").lower() == "true"
    )
    app.config["SESSION_COOKIE_SECURE"] = session_cookie_secure

    # Localhost ports are cross-origin but same-site; production Vercel and
    # Render hosts are cross-site and require SameSite=None over HTTPS.
    app.config["SESSION_COOKIE_SAMESITE"] = (
        "None" if session_cookie_secure else "Lax"
    )

    # ── INIT DB ───────────────────────────────────────────────────
    db.init_app(app)

    # Import database Models
    from .models import Note, User

    # Current working app model
    with app.app_context():
        db.create_all()

    # Register Notes route
    from .notes.routes import notes_bp
    app.register_blueprint(notes_bp)

    # Register Analysis route
    from .analysis.routes import analysis_bp
    app.register_blueprint(analysis_bp)

    # Register Docs route
    from .docs.routes import docs_bp
    app.register_blueprint(docs_bp)

    # Register plan route
    from .plan.routes import plan_bp
    app.register_blueprint(plan_bp)

    # Register codebase route
    from .codebase.routes import codebase_bp
    app.register_blueprint(codebase_bp)

    # Register auth route
    from .auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    return app