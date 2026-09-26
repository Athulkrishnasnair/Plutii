import zipfile

from flask import Blueprint, jsonify, request, session

from app.services.codebase_service import scan_project
from app.models import Codebase, CodebaseFile
from app.extensions import db
from app.services.codebase_ai_service import analyze_codebase

from app.services.codebase_service import (
    scan_project,
    extract_imports,
)

codebase_bp = Blueprint(
    "codebase",
    __name__,
    url_prefix="/api/codebase"
)

# Upload zip
@codebase_bp.route("/upload", methods=["POST"])
def upload_codebase():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Not authenticated"}), 401

    if "file" not in request.files:
        return jsonify({"error": "ZIP file is required."}), 400

    file = request.files["file"]

    if not file.filename.lower().endswith(".zip"):
        return jsonify({"error": "Only ZIP files are supported."}), 400

    try:
        files = scan_project(file.read())
        relationships = extract_imports(files)
        codebase = Codebase(
            user_id=user_id,
            name=file.filename
        )

        db.session.add(codebase)
        db.session.flush()

        for item in files:
            codebase_file = CodebaseFile(
                codebase_id=codebase.id,
                path=item["path"],
                size=item["size"],
                content=item["content"]
            )

            db.session.add(codebase_file)

        db.session.commit()

        return jsonify({
            "id": codebase.id,
            "name": codebase.name,
            "file_count": len(files),
            "files": [
                {
                    "path": item["path"],
                    "size": item["size"]
                }
                for item in files
            ],
            'relationships': relationships
        }), 200

    except zipfile.BadZipFile:
        db.session.rollback()

        return jsonify({
            "error": "Invalid ZIP file."
        }), 400

    except Exception as exc:
        db.session.rollback()

        return jsonify({
            "error": str(exc)
        }), 500

#  Analyzwe route
@codebase_bp.route("/analyze", methods=["POST"])
def analyze_codebase_route():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Not authenticated"}), 401

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must contain JSON."}), 400

    query = data.get("query")

    if not isinstance(query, str) or not query.strip():
        return jsonify({"error": "A question is required."}), 400

    codebase = (
        Codebase.query
        .filter_by(user_id=user_id)
        .order_by(Codebase.created_at.desc())
        .first()
    )

    if not codebase:
        return jsonify({
            "error": "Upload a project first."
        }), 400

    files = [
        {
            "path": file.path,
            "size": file.size,
            "content": file.content
        }
        for file in codebase.files
    ]

    try:
        result = analyze_codebase(
            query=query.strip(),
            files=files
        )

        return jsonify(result), 200

    except Exception as exc:
        return jsonify({
            "error": str(exc)
        }), 503