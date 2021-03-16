from flask_migrate import Migrate
from sqlalchemy import create_engine
from flask import Flask
from .main import main
from .models import *
import pandas as pd
from .ext import db
import os

# application factory method
def create_app():
    app = Flask(__name__)
    
    #* Make sure to set this env in Heroku: "heroku config:set FLASK_ENV=development"
    if os.environ['FLASK_ENV'] == "development": app.config.from_object("config.debug")
    else: app.config.from_object("config.prod")

    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(main)

    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

    # #* When Flask is run within the context of an app (using `flask run` or `flask db stamp head`), it checks if the database contains the Word table and if it is empty. If both conditions are fulfilled, then it fills in such table using the `words.csv` file. This should only happen once, when the server is initialised for the first time.
    # with app.app_context():
    if engine.dialect.has_table(engine, "Word") and not db.session.query(Word).first():
        print("Populating Words...")
        words_df = pd.read_csv('data/words.csv')
        words_df.to_sql("Word", engine, if_exists="append", index=False) #! This should never fail

    return app

# Useful commands for migration: flask db init, flask db migrate, flask db upgrade, flask db stamp head (in that order)
migrate = Migrate(compare_type=True)