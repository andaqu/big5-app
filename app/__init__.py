from models import base, personality, twitter
from .helper import document_model
from flask_migrate import Migrate
from flask import Flask
from .main import main
from .ext import db
import os

# application factory method
def create_app():
    app = Flask(__name__)
    
    #* Make sure to set this env in Heroku: "heroku config:set FLASK_ENV=development"
    # if os.environ['FLASK_ENV'] == "development": app.config.from_object("config.debug")
    # else: app.config.from_object("config.prod")
    app.config.from_object(CONFIG[os.getenv("FLASK_ENV")])

    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(main)

    return app

CONFIG = {"development" : "config.debug", "production": "config.prod", None : "config.debug"}

# Useful commands for migration: flask db init, flask db migrate, flask db upgrade, flask db stamp head (in that order)
migrate = Migrate(compare_type=True, include_schemas=True)