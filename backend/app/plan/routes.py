import json

from flask import Blueprint, jsonify, request, session

from app.services.plan_service import create_implementation_plan

from app.extensions import db
from app.models import Analysis


plan_bp = Blueprint(
    "plan",
    __name__,
    url_prefix="/api/plan"
)


@plan_bp.route("/analyze", methods=["POST"])
def analyze_plan():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "error": "Not authenticated"
        }), 401

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body must contain JSON."
        }), 400

    content = data.get("content")

    if not isinstance(content, str) or not content.strip():
        return jsonify({
            "error": "Content is required."
        }), 400

    if len(content) > 30000:
        return jsonify({
            "error": "Content is too long."
        }), 400

    try:
        result = create_implementation_plan(
            content=content.strip()
        )

        # Store
        analysis = Analysis(
        user_id=user_id,
        lens_type="plan",
        input_text=content.strip(),
        result=json.dumps(result)
        )

        db.session.add(analysis)
        db.session.commit()
        
        return jsonify(result), 200

    except RuntimeError as exc:
        return jsonify({
            "error": str(exc)
        }), 503