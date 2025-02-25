from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity, get_jwt,
    set_access_cookies, unset_jwt_cookies
)
from functools import wraps
from app.models import db, User
from datetime import timedelta
from flask_jwt_extended import JWTManager

auth = Blueprint('auth', __name__)


BLOCKLIST = set()


@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "User already exists"}), 400

    if data['role'] not in ['admin', 'staff', 'student']:
        return jsonify({"message": "Invalid role"}), 400

    new_user = User(username=data['username'], role=data['role'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": f"User {data['role']} registered successfully!"}), 201


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if not user or not user.check_password(data['password']):
        return jsonify({"message": "Invalid username or password"}), 401

    access_token = create_access_token(
        identity=str(user.id),  
        additional_claims={"role": user.role},  
        expires_delta=timedelta(hours=2)
    )

    
    response = make_response(jsonify({"message": "Login successful"}))
    set_access_cookies(response, access_token)  
    return response


@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = make_response(jsonify({"message": "Successfully logged out"}))
    unset_jwt_cookies(response)  
    return response


jwt = JWTManager()

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST  


def role_required(*required_role):
    def decorator(func):
        @wraps(func)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()  
            user_id = get_jwt_identity()  
            
            if "role" not in claims:
                return jsonify({"message": "Invalid token: Missing role"}), 401

            # if claims["role"] != required_role:
            #     return jsonify({"message": "Unauthorized access"}), 403

            return func(*args, **kwargs)

        return wrapper
    return decorator


@auth.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"message": "Access granted", "user": current_user}), 200


@auth.route('/admin-only', methods=['GET'])
@role_required("admin")
def admin_route():
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    return jsonify({"message": "Welcome, Admin!", "user_id": current_user_id, "role": claims["role"]}), 200


@auth.route('/staff-only', methods=['GET'])
@role_required("staff")
def staff_route():
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    return jsonify({"message": "Welcome, Staff!", "user_id": current_user_id, "role": claims["role"]}), 200


@auth.route('/student-only', methods=['GET'])
@role_required("student")
def student_route():
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    return jsonify({"message": "Welcome, Student!", "user_id": current_user_id, "role": claims["role"]}), 200

