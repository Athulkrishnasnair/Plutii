from flask import Blueprint, jsonify, request
from app.services.ai_service import analyze_error


analysis_bp = Blueprint(
    "analysis",
    __name__,
    url_prefix="/api/analysis",
)

# A route for Error feature which is can be ised for error correction
@analysis_bp.route("/error", methods=["POST"])
def analyze_error_route():
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
    result = analyze_error(
        error=error.strip(),
        code=code,
        context=code,
    )

    return jsonify(result), 200