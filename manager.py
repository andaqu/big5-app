from app import create_app, db, base, personality, twitter
from app.settings import DOCUMENT, USER
from sqlalchemy import create_engine
from flask_migrate import Manager
import pandas as pd
import time

app = create_app()
manager = Manager(app)
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])

@manager.command
def populate_words():
    # Check if table "Word" exists and if it is empty
    if engine.dialect.has_table(engine, "Word") and not db.session.query(base.Word).first():
        print("Populating words...")
        words_df = pd.read_csv("data/words.csv")
        words_df.to_sql("Word", engine, if_exists="append", index=False)
    else:
        print("Table 'Word' does not exist or is not empty. Migrate and try again.")

@manager.option("-s", "--schema", dest="schema", default="personality", help="Schema to featurise documents of")
@manager.option("-n", "--number", dest="n", help="Batch size to commit to database", default=100)
def featurise_documents(schema, n):
    try:
        n = int(n)
        document = DOCUMENT[schema]
    except:
        print("Revise parameters. Quitting...")
        return

    # Check if table "Document" exists within the specified schema
    if engine.dialect.has_table(engine, "Document", schema=schema):

        # Get documents which are not featurised
        empties = db.session.query(document).filter_by(features = None).all()
        N = len(empties)

        if N == 0:
            print("No documents to featurise.")
            return

        print(f"Featurising documents from [{schema}] schema and saving every [{n}] documents...")
        
        i = 0
        to_save = []

        t0 = time.time()

        for document in empties:
            document.compute_features()

            i += 1
            to_save.append(document)
            
            # Save the documents in `to_save` in batches of `n`
            if i == n:
                db.session.bulk_save_objects(to_save)
                db.session.commit()
                print(f"Featurised and saved {i}/{N} documents.")
                i = 0
                to_save = []

        db.session.bulk_save_objects(to_save)
        db.session.commit()
        print(f"Featurised and saved {i}/{N} documents.")
        
        t1 = time.time()

        print(f"Done! That took {(t1-t0)/60} minutes in total.")

    else:
        print(f"Table '{schema}.Document' does not exist. Migrate and try again.")

if __name__ == "__main__":
    manager.run()