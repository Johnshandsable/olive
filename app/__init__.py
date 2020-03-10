from flask import Flask, session
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate, MigrateCommand
from app.config import Config
# from logging import FileHandler, WARNING


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    migrate.init_app(app, db)
    from app.users.routes import users
    from app.main.routes import main
    from app.posts.routes import posts
    from app.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    """
    NOTE: NOT USED IN PRODUCTION
    if not app.debug:
        file_handler = FileHandler('errorlog.txt')
        file_handler.setLevel(WARNING)
        app.logger.addHandler(file_handler)
    """

    return app
