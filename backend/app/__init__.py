from flask import Flask 
from .extensions import db


def create_app():
    app = Flask(__name__)

    # Configure the db
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///plutti.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Connecting db to FLask app
    db.init_app(app)

    # Import Note table
    from .models import Note

    # Current working app model
    with app.app_context():
        db.create_all()

    # Register Notes route
    from .notes.routes import notes_bp
    app.register_blueprint(notes_bp)

    return app