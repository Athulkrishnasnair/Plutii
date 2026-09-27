from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


# Class for notes
class Note(db.Model):

    # Fields
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

    # Connect with user
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )

# Class for users (db table)
class User(db.Model):

    # Fields
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)

    # Connect note with user
    notes = db.relationship(
        "Note",
        backref="user",
        lazy=True
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Analysis model
class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    lens_type = db.Column(
        db.String(30),
        nullable=False
    )

    input_text = db.Column(
        db.Text,
        nullable=False
    )

    result = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    user = db.relationship(
        "User",
        backref=db.backref("analyses", lazy=True)
    )

# File zip storage
class Codebase(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    name = db.Column(db.String(255), nullable=False)

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    files = db.relationship(
        "CodebaseFile",
        backref="codebase",
        cascade="all, delete-orphan"
    )


class CodebaseFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    codebase_id = db.Column(
        db.Integer,
        db.ForeignKey("codebase.id"),
        nullable=False
    )

    path = db.Column(db.Text, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)