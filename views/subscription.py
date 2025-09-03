from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from extensions import db
from models.subscription import SubscriptionPlan, Subscription

subscription_blueprint = Blueprint("subscription", __name__)


@subscription_blueprint.route("/plan", methods=["POST"])
def create_subscription_blueprint():
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


@subscription_blueprint.route('/plan/<int:subscription_plan_id>', methods=["GET"])
def get_plan(subscription_plan_id):
    plan = SubscriptionPlan.query.get_or_404(subscription_plan_id)

    plan_data = {
        "id": plan.id,
        "plan_name": plan.plan_name,
        "cost": plan.cost,
        "months_duration": plan.months_duration
    }

    return jsonify(plan_data), 200


@subscription_blueprint.route("/plans", methods=["GET"])
def list_plans():
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


@subscription_blueprint.route("/subscribe", methods=["POST"])
@login_required
def subscribe():
    if current_user.subscription:
        return jsonify({
            "message": "User already have a subscription!",
        }), 400

    data = request.get_json()

    plan_id = data["plan_id"]
    plan = SubscriptionPlan.query.get(plan_id)

    if plan.id == 1:
        new_subscription = Subscription(
            plan_id=plan.id,
            user_id=current_user.id
        )
    else:
        current_date = datetime.now()

        new_subscription = Subscription(
            payment_start_date=current_date,
            payment_end_date=current_date +
            timedelta(days=plan.months_duration)
        )

    try:
        db.session.add(new_subscription)
        db.session.commit()

        return jsonify({
            "message": f"User {current_user.first_name} {current_user.last_name} subscribed correctly!",
            "subscription_id": f"{new_subscription.id}"
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@subscription_blueprint.route("/upgrade", methods=["PATCH"])
@login_required
def upgrade_subscription():
    if not current_user.subscription:
        return jsonify({
            "message": "User has no subscription!",
        }), 400

    subscription = current_user.subscription

    data = request.get_json()

    plan_id = data["plan_id"]
    plan = SubscriptionPlan.query.get(plan_id)

    # For this challenge plans are structured in ascending order
    # Such that the most exclusive plans have a higher ID
    # A user cannot downgrade their plan
    if subscription.plan.id >= plan.id:
        return jsonify({
            "message": "User already have this plan or a higher one!",
        }), 400

    if subscription.plan.id == 1:
        current_date = datetime.now()

        subscription.plan_id = plan_id
        subscription.payment_start_date = current_date
        subscription.payment_end_date = current_date + \
            timedelta(days=plan.months_duration)
    else:
        subscription.plan_id = plan_id
        subscription.payment_end_date += timedelta(days=plan.months_duration)

    try:
        db.session.commit()

        return jsonify({
            "message": f"Subscription {subscription.id} upgraded successfully!",
            "subscription": {
                "id": subscription.id,
                "start_date": subscription.start_date.isoformat() if subscription.start_date else None,
                "payment_start_date": subscription.payment_start_date.isoformat() if subscription.payment_start_date else None,
                "payment_end_date": subscription.payment_end_date.isoformat() if subscription.payment_end_date else None,
                "to_be_canceled": subscription.to_be_canceled,
                "active": subscription.active,
                "plan_id": subscription.plan_id,
                "user_id": subscription.user_id,
            }

        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@subscription_blueprint.route("/cancel", methods=["PATCH"])
@login_required
def cancel_subscription():
    if not current_user.subscription:
        return jsonify({
            "message": "User has no subscription!",
        }), 400

    if current_user.subscription.payment_start_date is None:
        current_user.subscription.active = False

        try:
            db.session.commit()

            return jsonify({
                "message": f"Subscription {current_user.subscription.id} has been canceled!"
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
    else:
        current_user.subscription.to_be_canceled = True

        try:
            db.session.commit()

            return jsonify({
                "message": f"Subscription {current_user.subscription.id} marked to be canceled once the paid period finishes!"
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
