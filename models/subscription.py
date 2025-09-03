from extensions import db


class SubscriptionPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plan_name = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    months_duration = db.Column(db.Integer, nullable=False)

    subscriptions = db.relationship(
        "Subscription", backref="plan", lazy="dynamic"
    )

    def __repr__(self):
        return f"<Plan Name: - {self.plan_name} - Cost: {self.cost} ({self.months_duration})>"


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, nullable=False, default=db.func.now())
    payment_start_date = db.Column(db.DateTime, nullable=True)
    payment_end_date = db.Column(db.DateTime, nullable=True)
    to_be_canceled = db.Column(db.Boolean, nullable=False, default=False)
    active = db.Column(db.Boolean, nullable=False, default=True)

    plan_id = db.Column(
        db.Integer,
        db.ForeignKey("subscription_plan.id"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False,
        unique=True
    )

    __table_args__ = (
        db.Index('ix_active', 'active'),
    )
