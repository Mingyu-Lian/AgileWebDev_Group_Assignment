from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from .config import Config
from .routes import main as main_blueprint
from app.models import User
from app.models import db


migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

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
        db.create_all()  # 创建或更新数据库表

    return app