from flask import Blueprint, jsonify, request
from app.models import Note
from app.extensions import db

# Name the bluwprint
notes_bp = Blueprint('notes', __name__, url_prefix="/api/notes")

# Creating notes Endpoint route
@notes_bp.route("", methods=["GET"])
def get_notes():

    # Query the entire db for the notes or content 
    notes = Note.query.all()

    # Pythonic way of traversing list of dicts 
    return jsonify([
        {
            "id": note.id,
            "title": note.title,
            "content": note.content
        }
        for note in notes
    ])


# Helper for validation
def validate_note(data):

    # data is a obj
     if not data:
         return "Invalid Note."

     if "title" not in data or "content" not in data:
         return "Title and content are required"

     if not isinstance(data['title'], str):
         return "Title must be text"

     if not isinstance(data['content'], str):
         return "content must be text"

     if not data['title'].strip():
         return "Title cannot be empty"

     if not data['content'].strip():
         return "Content cannot be empty"

     if len(data["title"]) > 200:
         return "Invalid title length"

     return None


# Post Method create notes
@notes_bp.route("", methods=["POST"])
def create_notes():
    data = request.get_json()

    # Validation
    error = validate_note(data)

    if error:
        return jsonify(
            {
                "error": error
            }
        ), 400


    note = Note(
        title = data["title"],
        content = data["content"]
    )

    # Add note to db

    db.session.add(note)
    db.session.commit()

    # Return json
    return jsonify({
        "id": note.id,
        "title": note.title,
        "content": note.content
    }), 201

# Get a specific note
@notes_bp.route("/<int:note_id>", methods=["GET"])
def get_note(note_id):

    note = db.get_or_404(Note, note_id)
    return jsonify({
        "id": note.id,
        "title": note.title,
        "content": note.content
    })

# Replace notes with PUT
@notes_bp.route("/<int:note_id>", methods=["PUT"])
def update_note(note_id):

    note = db.get_or_404(Note, note_id)
    data = request.get_json()

    error = validate_note(data)

    if error:
        return jsonify(
            {
                "error": error
            }
        ), 400

    # Update note
    note.title = data["title"]
    note.content = data["content"]

    db.session.commit()

    return jsonify({
         "id": note.id,
         "title": note.title,
         "content": note.content
    })

# Delete a note
@notes_bp.route("/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):

    note = db.get_or_404(Note, note_id)

    db.session.delete(note)
    db.session.commit()
    return jsonify({
        "message": "Note deleted sucessfully"
    })