from app import create_app, db, base, twitter, document_model
from sqlalchemy import create_engine
from flask_migrate import Manager
from bot import Tweety
import pandas as pd
import time

app = create_app()
manager = Manager(app)
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])

@manager.command
def populate_words():
    # Check if table "Word" exists and if it is empty
    if not (engine.dialect.has_table(engine, "Word") and not db.session.query(base.Word).first()):
        print("Table 'Word' does not exist or is not empty. Migrate and try again.")
        return

    print("Populating words...")
    words_df = pd.read_csv("data/words.csv")
    words_df.to_sql("Word", engine, if_exists="append", index=False)

@manager.option("-s", "--schema", dest="schema", default="personality", help="Schema to featurise documents of.")
@manager.option("-b", "--batch_size", dest="b", help="Batch size to commit to database.", default=100)
def featurise_documents(schema, b):
    try:
        b = int(b)
        Document = document_model[schema]
    except:
        print("Revise parameters. Quitting...")
        return

    # Check if table "Document" exists within the specified schema
    if not engine.dialect.has_table(engine, "Document", schema=schema):
        print(f"Table '{schema}.Document' does not exist. Migrate and try again.")
        return

    # Get documents which are not featurised
    empties = db.session.query(Document).filter(Document.features == None).filter(Document.text != "").all()
    N = len(empties)

    if N == 0:
        print("No documents to featurise.")
        return

    print(f"Featurising [{N}] documents from [{schema}] schema and saving every [{b}] documents...")
    
    i = 0
    to_save = []

    t0 = time.time()

    for document in empties:
        document.compute_features()

        i += 1
        to_save.append(document)
        
        # Save the documents in `to_save` in batches of `b`
        if not(i % b):
            db.session.bulk_save_objects(to_save)
            db.session.commit()
            print(f"*** Featurised and saved {i}/{N} documents. ***")
            to_save = []

    if len(to_save) != 0:
        db.session.bulk_save_objects(to_save)
        db.session.commit()
        print(f"*** Featurised and saved {i}/{N} documents. ***")
    
    t1 = time.time()

    print(f"Done! That took {(t1-t0)/60} minutes in total.")

@manager.option("-n", "--tweets", dest="n", help="Number of tweets to extract from every user.", default=400)
@manager.option("-b", "--batch_size", dest="b", help="Batch size to commit to database.", default=100)
def get_tweets(n, b):

    try:
        n = int(n)
        b = int(b)
    except:
        print("Revise parameters. Quitting...")
        return

    if not engine.dialect.has_table(engine, "Document", schema="twitter"):
        print(f"Table 'twitter.Document' does not exist. Migrate and try again.")
        return

    tweety = Tweety(tweets_to_extract=n)
        
    docs = twitter.Document.query.all()
    N = len(docs)

    i = 0
    to_save = []

    t0 = time.time()

    for document in docs:

        new_doc = tweety.get_document(document.id, stored_tweets=document.stored_tweets, first=document.first, last=document.last)

        if not new_doc["valid"]:
            print(new_doc["output"])
            continue

        print(f"User [{document.id}]: Retrieved {n} tweets.")

        new_doc = new_doc["output"]

        document.text += new_doc["text"] + " "
        document.features = None # Since the text was updated, re-initialise the features list
        document.stored_tweets = new_doc["stored_tweets"]
        document.first = new_doc["first"]
        document.last = new_doc["last"]

        i += 1
        to_save.append(document)

        # Save the documents in `to_save` in batches of `b`
        if not(i % b) and len(to_save) != 0:
            db.session.bulk_save_objects(to_save)
            db.session.commit()
            print(f"=== Stored the documents of {i}/{N} users. ===")
            to_save = []
    
    if len(to_save) != 0:
        db.session.bulk_save_objects(to_save)
        db.session.commit()
        print(f"=== Stored the documents of {i}/{N} users. ===")

    t1 = time.time()

    print(f"Done! That took {(t1-t0)/3600} hours in total.")

    return

if __name__ == "__main__":
    manager.run()