from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from .routes import main as main_blueprint
from app.models import User
from app.models import db
from app.config import DevelopmentConfig, TestingConfig



migrate = Migrate()
login_manager = LoginManager()


def create_app(Config_Name=DevelopmentConfig):
    app = Flask(__name__)
    if Config_Name == 'testing':
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    login_manager.login_view = 'main.login'

    login_manager.login_view = 'login'

    with app.app_context():
        from . import routes, models
        db.create_all()

    return app
