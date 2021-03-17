import pandas as pd
from app import create_app, db
from app.models import *
from flask_migrate import MigrateCommand, Manager
from sqlalchemy import create_engine
import time

app = create_app()
manager = Manager(app)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

@manager.command
def populate_words():

    if engine.dialect.has_table(engine, "Word") and not db.session.query(Word).first():
        print("Populating words...")
        words_df = pd.read_csv('data/words.csv')
        words_df.to_sql("Word", engine, if_exists="append", index=False)
    else:
        print("Table 'Word' does not exist or is not empty. Migrate and try again.")

@manager.command
def featurise_documents():
    
    if engine.dialect.has_table(engine, "Document"):

        empties = db.session.query(Document).filter_by(features = None).all()

        if len(empties) == 0:
            print("No documents to featurise.")
            return

        print("Featurising documents...")
        
        t0 = time.time()
        for document in empties:
            document.compute_features()
        t1 = time.time()

        print(f"Done! That took {t1-t0} seconds.")

        db.session.bulk_save_objects(empties)
        db.session.commit()
        
    else:
        print("Table 'Document' does not exist. Migrate and try again.")

if __name__ == "__main__":
    manager.run()