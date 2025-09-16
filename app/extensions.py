from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
jwt = JWTManager()
ma = Marshmallow()
login_manager = LoginManager()
migrate = Migrate()

def init_extensions(app):
    db.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)