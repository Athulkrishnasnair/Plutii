from flask import Flask 
from .extensions import db
from flask_cors import CORS

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

    # Register auth route
    from .auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    return app