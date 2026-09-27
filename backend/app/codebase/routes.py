import io
import re
import zipfile
import requests
from flask import Blueprint, jsonify, request, session

from app.models import Codebase, CodebaseFile
from app.extensions import db
from app.services.codebase_service import (
    scan_project,
    extract_imports,
)
from app.services.codebase_ai_service import (
    analyze_codebase,
    explain_file,
    explain_selection,
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
            "relationships": relationships
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


# Import public GitHub repository
@codebase_bp.route("/github", methods=["POST"])
def import_github_codebase():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Not authenticated"}), 401

    data = request.get_json(silent=True)

    if not data or not isinstance(data, dict):
        return jsonify({"error": "Request body must contain JSON with 'url'."}), 400

    url = data.get("url")

    if not url or not isinstance(url, str) or not url.strip():
        return jsonify({"error": "A GitHub repository URL is required."}), 400

    url = url.strip()

    # Match https://github.com/owner/repo or https://github.com/owner/repo/ (with optional .git)
    match = re.match(
        r"^https?://github\.com/([a-zA-Z0-9_.-]+)/([a-zA-Z0-9_.-]+?)(?:\.git)?/?$",
        url
    )

    if not match:
        return jsonify({
            "error": "Invalid GitHub repository URL. Expected format: https://github.com/owner/repository"
        }), 400

    owner, repo = match.groups()
    if repo.endswith(".git"):
        repo = repo[:-4]

    repo_name = f"{owner}/{repo}"

    # Public GitHub zip archive endpoint
    archive_url = f"https://github.com/{owner}/{repo}/archive/HEAD.zip"

    try:
        resp = requests.get(
            archive_url,
            timeout=25,
            allow_redirects=True,
            headers={
                "User-Agent": "ArrowLens/1.0"
            }
        )
    except requests.exceptions.Timeout:
        return jsonify({"error": "GitHub repository download timed out. Please try again."}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to connect to GitHub: {str(e)}"}), 502

    if resp.status_code == 404:
        return jsonify({"error": f"Repository '{repo_name}' not found or is private on GitHub."}), 404
    elif resp.status_code != 200:
        return jsonify({"error": f"GitHub returned HTTP status {resp.status_code}."}), 400

    zip_bytes = resp.content
    if not zip_bytes:
        return jsonify({"error": "Downloaded repository archive was empty."}), 400

    try:
        files = scan_project(zip_bytes)
        if not files:
            return jsonify({
                "error": "No supported source files (.py, .js, .ts, .vue, .json, .md, etc.) found in repository."
            }), 400

        relationships = extract_imports(files)

        codebase = Codebase(
            user_id=user_id,
            name=repo_name
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
            "relationships": relationships
        }), 200

    except zipfile.BadZipFile:
        db.session.rollback()
        return jsonify({
            "error": "The downloaded repository archive was not a valid ZIP file."
        }), 400
    except Exception as exc:
        db.session.rollback()
        return jsonify({
            "error": str(exc)
        }), 500


# Get single file content
@codebase_bp.route("/file", methods=["GET"])
def get_codebase_file():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Not authenticated"}), 401

    path = request.args.get("path")
    if not path or not path.strip():
        return jsonify({"error": "File path parameter is required."}), 400

    path = path.strip()
    codebase_id = request.args.get("codebase_id", type=int)

    query = Codebase.query.filter_by(user_id=user_id)
    if codebase_id:
        codebase = query.filter_by(id=codebase_id).first()
    else:
        codebase = query.order_by(Codebase.created_at.desc()).first()

    if not codebase:
        return jsonify({"error": "No codebase found for this user."}), 404

    file_record = CodebaseFile.query.filter_by(codebase_id=codebase.id, path=path).first()
    if not file_record:
        return jsonify({"error": f"File '{path}' not found in codebase."}), 404

    return jsonify({
        "id": file_record.id,
        "codebase_id": codebase.id,
        "path": file_record.path,
        "size": file_record.size,
        "content": file_record.content
    }), 200


# Explain file or selection
@codebase_bp.route("/explain", methods=["POST"])
def explain_codebase_code():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Not authenticated"}), 401

    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        return jsonify({"error": "Request body must contain JSON."}), 400

    file_path = data.get("file_path")
    if not file_path or not isinstance(file_path, str) or not file_path.strip():
        return jsonify({"error": "Field 'file_path' is required."}), 400

    file_path = file_path.strip()
    codebase_id = data.get("codebase_id")

    query = Codebase.query.filter_by(user_id=user_id)
    if codebase_id:
        codebase = query.filter_by(id=codebase_id).first()
    else:
        codebase = query.order_by(Codebase.created_at.desc()).first()

    if not codebase:
        return jsonify({"error": "No codebase found."}), 404

    file_record = CodebaseFile.query.filter_by(codebase_id=codebase.id, path=file_path).first()
    if not file_record:
        return jsonify({"error": f"File '{file_path}' not found in codebase."}), 404

    scope = data.get("scope", "selection" if "start_line" in data else "file")

    try:
        if scope == "selection":
            start_line = data.get("start_line", 1)
            end_line = data.get("end_line", start_line)

            try:
                start_line = max(1, int(start_line))
                end_line = max(start_line, int(end_line))
            except (ValueError, TypeError):
                start_line, end_line = 1, 1

            lines = file_record.content.splitlines()
            total_lines = len(lines)
            end_line = min(end_line, max(1, total_lines))

            # Extract selected code if not provided
            selected_code = data.get("code")
            if not selected_code:
                selected_lines = lines[start_line - 1 : end_line]
                selected_code = "\n".join(selected_lines)

            result = explain_selection(
                file_path=file_path,
                selected_code=selected_code,
                start_line=start_line,
                end_line=end_line,
                surrounding_context=file_record.content
            )
        else:
            result = explain_file(
                file_path=file_path,
                content=file_record.content
            )

        return jsonify(result), 200

    except Exception as exc:
        return jsonify({
            "error": str(exc)
        }), 503


# Analyze route
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