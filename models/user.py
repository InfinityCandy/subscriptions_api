from extensions import db
import enum
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.types import TypeDecorator, String


class UserType(enum.Enum):
    ADMIN = 'admin'
    REGULAR = 'regular'


class UserTypeEnum(TypeDecorator):
    impl = String(10)

    def process_bind_param(self, value, dialect):
        if isinstance(value, UserType):
            return value.value
        return value

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return UserType(value)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(254), nullable=False)
    last_name = db.Column(db.String(254), nullable=False)

    user_type = db.Column(
        UserTypeEnum,
        nullable=False,
        default=UserType.REGULAR
    )

    subscription = db.relationship(
        "Subscription",
        backref="User",
        uselist=False,
        lazy=True,
        cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<Email: - {self.email} - Name: {self.first_name} {self.last_name}>"
