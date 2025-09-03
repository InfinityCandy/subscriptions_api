from flask_login import login_user, logout_user, login_required, current_user
from flask import Blueprint, request, jsonify
from models.user import User

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    user = User.query.filter_by(email=data['email']).first()
    if user is None or not user.check_password(data['password']):
        return jsonify({"error": "Invalid email or password"}), 401

    login_user(user)
    return jsonify({"message": "Logged in successfully!"}), 200


@auth_blueprint.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully!"}), 200


@auth_blueprint.route('/profile')
@login_required
def profile():
    return jsonify({
        "message": f"Welcome, {current_user.email}!",
        "email": current_user.email
    }), 200
