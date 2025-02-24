from flask import Flask
from flask_jwt_extended import JWTManager
from app.config import Config
from app.extensions import db, migrate, ma
from app.routes import main
from app.auth import auth

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)  

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(main)

    return app
