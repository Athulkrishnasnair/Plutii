from flask import Blueprint

# Name the bluwprint
notes_bp = Blueprint('notes', __name__)

# Creating notes Endpoint route
@notes_bp.get("/api/notes")
def get_notes():
    return {"message": "Notes endpoint works!"}