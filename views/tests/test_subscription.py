import pytest
from faker import Faker
from app import app, db
from models.user import User, UserType
from models.subscription import Subscription, SubscriptionPlan
from flask_login import login_user

fake = Faker()


@pytest.fixture(scope="module")
def app_with_db():
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app_with_db):
    return app_with_db.test_client()


@pytest.fixture
def user_data(app_with_db):
    user = User(
        email=fake.email(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        user_type=UserType.ADMIN,
    )
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def logged_in_client(client, user_data, app_with_db):
    with app_with_db.test_request_context():
        login_user(user_data)

    return client


@pytest.fixture
def setup_subscriptions(app_with_db):
    plan = SubscriptionPlan(
        plan_name="Pro",
        cost=3.99,
        months_duration=3
    )
    db.session.add(plan)

    user_one = User(
        email=fake.email(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        user_type=UserType.REGULAR
    )
    user_one.set_password('password_one')
    db.session.add(user_one)

    user_two = User(
        email=fake.email(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        user_type=UserType.REGULAR
    )
    user_two.set_password('password_two')
    db.session.add(user_two)
    db.session.flush()

    active_sub_one = Subscription(
        active=True,
        plan_id=plan.id,
        user_id=user_one.id
    )
    db.session.add(active_sub_one)

    active_sub_two = Subscription(
        active=True,
        plan_id=plan.id,
        user_id=user_two.id
    )
    db.session.add(active_sub_two)

    user_inactive = User(
        email=fake.email(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        user_type=UserType.REGULAR
    )
    user_inactive.set_password('password_inactive')
    db.session.add(user_inactive)
    db.session.flush()

    inactive_sub = Subscription(
        active=False,
        plan_id=plan.id,
        user_id=user_inactive.id
    )
    db.session.add(inactive_sub)

    db.session.commit()


def test_list_active_subscriptions(logged_in_client, setup_subscriptions):
    response = logged_in_client.get('/subscription/active_subscriptions')
    response_data = response.get_json()

    assert response.status_code == 200
    assert len(response_data) == 2
