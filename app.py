from flask import Flask
from config import Config
from extensions import db, migrate, login_manager
from models.user import User
from models.subscription import SubscriptionPlan
from views.user import user_blueprint
from views.auth import auth_blueprint
from views.subscription import subscription_blueprint


app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# @app.shell_context_processor
# def make_shell_context():
#     return dict(db=db, User=User)


app.register_blueprint(user_blueprint, url_prefix="/user")
app.register_blueprint(auth_blueprint, url_prefix="/auth")
app.register_blueprint(subscription_blueprint, url_prefix="/subscription")
