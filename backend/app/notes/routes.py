from flask import Blueprint, jsonify, request, session
from app.models import Note
from app.extensions import db

# Name the bluwprint
notes_bp = Blueprint('notes', __name__, url_prefix="/api/notes")

# Creating notes Endpoint route
@notes_bp.route("", methods=["GET"])
def get_notes():
    # Collect session_id
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "error": "Not authenticated"
        }), 401

    # Filter db by session
    notes = Note.query.filter_by(user_id=user_id).all()

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

    user_id = session.get("user_id")
    if not user_id:
        return jsonify({
            "error": "Not authenticated"
        }), 401

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
        content = data["content"],
        user_id=user_id
    )

    
    # For creation of a note im am creating the ownership 
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

    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "error": "Not authenticated"
        }), 401

    # Gets the note
    note = db.session.get(Note, note_id)
    if not note:
        return jsonify({
            "error": "Note not found"
        }), 404

    # Check for users note session 
    if note.user_id != user_id:
        return jsonify({
            "error": "Not authorised"
        }), 403

    return jsonify({
        "id": note.id,
        "title": note.title,
        "content": note.content
    })

# Replace/update notes with PUT
@notes_bp.route("/<int:note_id>", methods=["PUT"])
def update_note(note_id):

    user_id = session.get("user_id")
    if not user_id:
        return jsonify({
            "error": "Not authenticated"
        }), 401

    note = db.session.get(Note, note_id)
    if not note:
        return jsonify({
            "error": "Note not found"
        }), 404

    if note.user_id != user_id:
        return jsonify({
            "error": "Not authorised"
        }), 403

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

    user_id = session.get("user_id")
    if not user_id:
        return jsonify({
            "error": "Not authenticated"
        }), 401

    note = db.session.get(Note, note_id)
    if not note:
        return jsonify({
            "error": "Note not found"
        }), 404

    if note.user_id != user_id:
        return jsonify({
            "error": "Not authorised"
        }), 403

    db.session.delete(note)
    db.session.commit()
    return jsonify({
        "message": "Note deleted successfully"
    })