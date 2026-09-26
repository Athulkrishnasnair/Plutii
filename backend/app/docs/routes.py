from flask import Blueprint, jsonify, request, session
from app.services.docs_service import analyze_docs
import json
import requests
from app.extensions import db
from app.models import Analysis
from app.services.web_service import fetch_web_content



docs_bp = Blueprint(
    "docs",
    __name__,
    url_prefix="/api/docs",
)

# Analyse route
@docs_bp.route("/analyze", methods=["POST"])
def analyze_docs_route():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "error": "Not authenticated"
        }), 401

    # Read the JSON

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body must contain JSON"
        }), 400

    # Get the content
    content = data.get("content")
    
    if not isinstance(content, str) or not content.strip():
        return jsonify({
            "error": "Documentation content is required"
        }), 400

    content = content.strip()

    # Adding a size limit
    if len(content) > 30000:
        return jsonify({
            "error": "Documentation is too large."
                     "Please provide a smaller section."
        }), 400

    # Call the api service
    try:
        result = analyze_docs(content)

        # Store res
        analysis = Analysis(
        user_id=user_id,
        lens_type="docs",
        input_text=content,
        result=json.dumps(result)
        )


        db.session.add(analysis)
        db.session.commit()


    except RuntimeError as exc:
        return jsonify({
            "error": str(exc)
        }), 503

    return jsonify(result), 200

# Web scraper
@docs_bp.route("/fetch", methods=["POST"])
def fetch_docs():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Not authenticated"}), 401

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must contain JSON."}), 400

    url = data.get("url")

    if not isinstance(url, str) or not url.strip():
        return jsonify({"error": "URL is required."}), 400

    try:
        result = fetch_web_content(url.strip())

        return jsonify(result), 200

    except requests.RequestException:
        return jsonify({"error": "Could not fetch this URL."}), 400