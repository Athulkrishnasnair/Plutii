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

# Post Method create notes
@notes_bp.route("", methods=["POST"])
def create_notes():
    data = request.get_json()

    # Validation
    if not data or "title" not in data or "content" not in data:
        return jsonify({
            "error": "title and content are required"
        }), 400


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

    if not data or "title" not in data or "content" not in data:
        return jsonify({
                "error": "title and content are required"
            }), 400

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