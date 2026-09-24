from flask import Blueprint, jsonify, request, session
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

# Login route
@auth_bp.route('/login', methods=["POST"])
def login():
     data = request.get_json()

    #  Validate data
     if not data:
          return jsonify({
               "error": "Request body is required"
          }), 400

     password = data.get("password")
     email = data.get("email")

     if not email or not password:
          return jsonify({
               "error": "Email and password are required"
          }), 400

    # Query the user
     user = User.query.filter_by(email=email).first()

    #  Check user and password
     if not user or not user.check_password(password):
          return jsonify({
               "error": "Invalid email or password"
          }), 401

    #  Store the user session 
     session["user_id"] = user.id

    # Sucess
     return({
          "message": "Login successful",
          "user": {
               "id": user.id,
               "username": user.username,
               "email": user.email
          }
     })

# Route about the user
@auth_bp.route("/me", methods=["GET"])
def get_current_user():

     # print("SESSION: ", dict(session))

     # Retrive session id
     user_id = session.get("user_id")

     if not user_id:
          return jsonify({
               "error": "Not authenticated"
          }), 401

     # Get user details
     user = db.session.get(User, user_id)

     return jsonify({
          "id": user.id,
          "username": user.username,
          "email": user.email
     })

# Logout route
@auth_bp.route("/logout", methods=["POST"])
def logout():
     session.clear()

     return jsonify({
          "message": "Logout successful"
     })