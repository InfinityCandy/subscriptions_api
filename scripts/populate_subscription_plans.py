from app import app, db
from models.subscription import SubscriptionPlan

app.app_context().push()


def populate_subscription_plans():
    plans_to_add = [
        {"id": 1, "plan_name": "Free", "cost": 0.0, "months_duration": 1},
        {"id": 2, "plan_name": "Pro", "cost": 3.99, "months_duration": 3},
        {"id": 3, "plan_name": "Premium", "cost": 12.99, "months_duration": 12}
    ]

    for plan_data in plans_to_add:
        existing_plan = SubscriptionPlan.query.filter_by(
            plan_name=plan_data["plan_name"]
        ).first()
        if existing_plan:
            print(f"Skipping {plan_data['plan_name']} plan")
        else:
            new_plan = SubscriptionPlan(
                id=plan_data['id'],
                plan_name=plan_data['plan_name'],
                cost=plan_data["cost"],
                months_duration=plan_data["months_duration"]
            )
            db.session.add(new_plan)
            print(f"Adding {plan_data['plan_name']} plan")

    try:
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    populate_subscription_plans()
