from flask import Flask 
from dotenv import load_dotenv
from .extensions import db
from flask_cors import CORS


load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app,
         supports_credentials=True,
         origins=["http://localhost:5173"]
         )

    # Configure the db
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///plutii.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Configure the session key
    app.config["SECRET_KEY"] = "dev-secret-key"

    # Allow the session cookie to be sent on cross-origin requests
    # (frontend on :5173, backend on :5000 are different origins).
    # SameSite=None is required for credentials to be included in
    # cross-origin fetch calls; Secure=False is intentional for local dev.
    # app.config["SESSION_COOKIE_SAMESITE"] = "None"
    # app.config["SESSION_COOKIE_SECURE"] = False

    

    # Connecting db to FLask app
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