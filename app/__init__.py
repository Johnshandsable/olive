from flask import Flask, session
from flask_marshmallow import Marshmallow
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from logging import FileHandler, WARNING

# CONFIGURATION
app = Flask(__name__)
app.config.from_object(Config)
ma = Marshmallow(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

if not app.debug:
    file_handler = FileHandler('errorlog.txt')
    file_handler.setLevel(WARNING)
    app.logger.addHandler(file_handler)

from app import routes, models
db.create_all()
