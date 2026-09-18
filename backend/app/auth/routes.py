from flask import Blueprint, jsonify, request
from app.models import User
from app.extensions import db

# Create a decorator fn for routes
auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth"
)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    # Validate request body
    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    # Get the info of users
    username = data.get('username')
    email=data.get('email')
    password=data.get('password')

    # Check password and username
    if not username or not email or not password:
        return jsonify({
            "error": "Username, email, password are required"
        }), 400

    # Search for existence
    if User.query.filter_by(username=username).first():
        return jsonify({
            "error": "Username already exists"
        }), 409

    if User.query.filter_by(email=email).first():
            return jsonify({
                "error": "Email already exists"
            }), 409

    # Else login the user
    user = User(
         username=username,
         email=email
    )

    user.set_password(password)

    # Add to db
    db.session.add(user)
    db.session.commit()

    # Sucess
    return jsonify({
         "message": "User registered successfully",
         "user": {
              "id": user.id,
              "username": user.username,
              "email": user.email
         }
    }), 201