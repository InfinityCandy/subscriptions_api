from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from models.user import UserType
from extensions import db
from models.subscription import SubscriptionPlan


plan_blueprint = Blueprint("plan", __name__)


@plan_blueprint.route("/", methods=["POST"])
@login_required
def create_plan():
    if not current_user.user_type == UserType.ADMIN:
        return jsonify({
            "message": "Unauthorized user!",
        }), 401

    data = request.get_json()

    plan_name = data["plan_name"]
    cost = data["cost"]
    months_duration = data["months_duration"]

    new_subscription_plan = SubscriptionPlan(
        plan_name=plan_name,
        cost=cost,
        months_duration=months_duration
    )

    try:
        db.session.add(new_subscription_plan)
        db.session.commit()

        return jsonify({
            "message": "Subscription Plan registered successfully!",
            "user_id": new_subscription_plan.id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@plan_blueprint.route('/<int:subscription_plan_id>', methods=["GET"])
@login_required
def get_plan(subscription_plan_id):
    plan = SubscriptionPlan.query.get_or_404(subscription_plan_id)

    plan_data = {
        "id": plan.id,
        "plan_name": plan.plan_name,
        "cost": plan.cost,
        "months_duration": plan.months_duration
    }

    return jsonify(plan_data), 200


@plan_blueprint.route("/plans", methods=["GET"])
@login_required
def list_plans():
    if not current_user.user_type == UserType.ADMIN:
        return jsonify({
            "message": "Unauthorized user!",
        }), 401

    plans = SubscriptionPlan.query.all()

    plans_list = []
    for plan in plans:
        plans_list.append({
            "id": plan.id,
            "plan_name": plan.plan_name,
            "cost": plan.cost,
            "months_duration": plan.months_duration
        })

    return jsonify(plans_list), 200
