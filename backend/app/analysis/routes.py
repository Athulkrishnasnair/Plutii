import json

from flask import Blueprint, jsonify, request, session

from app.extensions import db
from app.models import Analysis

from app.services.ai_service import analyze_error


analysis_bp = Blueprint(
    "analysis",
    __name__,
    url_prefix="/api/analysis",
)

# A route for Error feature which is can be ised for error correction
@analysis_bp.route("/error", methods=["POST"])
def analyze_error_route():
    # Require an authenticated session before doing anything else
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not authenticated"}), 401

    data = request.get_json(silent=True)

    # VAlidate
    if not data:
        return jsonify({
            "error": "Request body must contain JSON"
        }), 400

    error = data.get("error")

    # Check for empty error
    if not isinstance(error, str) or not error.strip():
        return jsonify({
            "error": "An error message is required"
        }), 400

    # Do the same for code and user context
    code = data.get("code", "")
    context = data.get("context", "")

    if not isinstance(code, str):
        return jsonify({
            "error": "Code must be text."
        }), 400

    if not isinstance(context, str):
        return jsonify({
            "error": "Context must be text."
        }), 400


    # Analyse the result
    try:
        result = analyze_error(
            error=error.strip(),
            code=code,
            context=context,
        )

        # Store
        analysis = Analysis(
        user_id=user_id,
        lens_type="error",
        input_text=error.strip(),
        result=json.dumps(result)
        )

        db.session.add(analysis)
        db.session.commit()

    except RuntimeError as exc:
        return jsonify({"error": str(exc)}), 503

    return jsonify(result), 200

# Get History
@analysis_bp.route("/history", methods=["GET"])
def get_analysis_history():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Not authenticated"}), 401

    analyses = (
        Analysis.query
        .filter_by(user_id=user_id)
        .order_by(Analysis.created_at.desc())
        .limit(20)
        .all()
    )

    history = []

    for analysis in analyses:
        history.append({
            "id": analysis.id,
            "lens_type": analysis.lens_type,
            "input": analysis.input_text,
            "result": json.loads(analysis.result),
            "created_at": analysis.created_at.isoformat()
        })

    return jsonify(history), 200


@analysis_bp.route("/<int:analysis_id>", methods=["DELETE"])
def delete_analysis(analysis_id):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not authenticated"}), 401

    analysis = db.session.get(Analysis, analysis_id)
    if not analysis or analysis.user_id != user_id:
        return jsonify({"error": "Analysis not found"}), 404

    db.session.delete(analysis)
    db.session.commit()

    return jsonify({"success": True}), 200