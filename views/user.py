from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User

user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/", methods=["POST"])
def create_user():
    data = request.get_json()

    email = data["email"]
    first_name = data["first_name"]
    last_name = data["last_name"]
    password = data["password"]

    existing_user = User.query.filter(User.email == email).first()
    if existing_user:
        return jsonify(
            {
                "error": "User with this username or email already exists"
            }
        ), 409

    new_user = User(
        email=email,
        first_name=first_name,
        last_name=last_name
    )
    new_user.set_password(password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            "message": "User registered successfully!",
            "user_id": new_user.id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
