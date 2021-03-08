from flask_migrate import Migrate
from flask import Flask
from .main import main
from .ext import db
import os

# application factory method
def create_app():
    app = Flask(__name__)
    
    if os.environ['FLASK_ENV'] == "development": app.config.from_object("config.debug")
    else: app.config.from_object("config.prod")

    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(main)

    return app

# Useful commands for migration: flask db init, flask db migrate, flask db upgrade, flask db stamp head (in that order)
migrate = Migrate()