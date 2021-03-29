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

@manager.option("-s", "--schema", dest="s", default="personality", help="Schema to featurise documents of.")
@manager.option("-b", "--batch_size", dest="b", help="Batch size to commit to database.", default=100)
def featurise_documents(s, b):

    # Check if parameters are valid
    try:
        b = int(b)
        Document = document_model[s]
    except:
        print("Revise parameters. Quitting...")
        return

    # Check if table "Document" exists within the specified schema
    if not engine.dialect.has_table(engine, "Document", schema=s):
        print(f"Table '{s}.Document' does not exist. Migrate and try again.")
        return

    # Get documents which are not featurised
    empties = db.session.query(Document).filter(Document.features == None).filter(Document.text != "").all()
    N = len(empties)

    if N == 0:
        print("No documents to featurise.")
        return

    print(f"Featurising [{N}] documents from [{s}] schema and saving every [{b}] documents...")
    
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
@manager.option("-a", "--all", dest="all", help="Retrieve tweets of every user in database (restarting the process)", default=True)
def get_tweets(n, b, all):

    # Check if parameters are valid
    try:
        n = int(n)
        b = int(b)
        all = bool(int(all))
    except:
        print("Revise parameters. Quitting...")
        return

    # Check if table "Document" exists within the specified schema
    if not engine.dialect.has_table(engine, "Document", schema="twitter"):
        print(f"Table 'twitter.Document' does not exist. Migrate and try again.")
        return

    # Initialise Tweety
    tweety = Tweety(tweets_to_extract=n)

    if not all:
        # Get document rows which have an empty text field and order them by ID
        docs = db.session.query(twitter.Document).filter(twitter.Document.text == "").order_by(twitter.Document.id).all()
        N = len(docs)

        if N == 0:
            print("All of the users have a text field. Set the --all parameter to False to consider all users. Quitting...")
            return

        update_documents(tweety, docs, N, save_every=b)
    else:
        # If the --all mode is enabled, every user will have their 'document' updated (Due to memory limitations, they will be extracted in batches)
        N = db.session.query(twitter.Document).count()

        LIMIT = b
        OFFSET = 0
        docs = db.session.query(twitter.Document).limit(LIMIT).offset(OFFSET).all()

        while len(docs) > 0:
            update_documents(tweety, docs, N, save_every=b)
            OFFSET += LIMIT
            docs = db.session.query(twitter.Document).limit(LIMIT).offset(OFFSET).all()

    return

def update_documents(tweety:Tweety, docs, N:int, save_every:int):
    """
    :tweety: Tweety instance
    :docs: List of documents from Document table
    :N: Total length of Document table
    :save_every: Add to database in batches of save_every
    """ 

    i = 0
    to_save = []

    for d in docs:

        backoff = 0.1

        # tweety.get_document is covered in an infinite loop in the cases where the bot requires us to sleep due to an
        # interrupted / disallowed connection (not talking about rate limits here), sleeping for `backoff` and trying
        # the retrieving the same document again.
        while True:

            new_doc = tweety.get_document(d.id, stored_tweets=d.stored_tweets, first=d.first, last=d.last)

            # If Tweety requires us to sleep, then do so
            if new_doc["sleep"]:
                print(new_doc["output"])

                timeout = 60 * backoff
                
                print(f"Due to a weird error, sleeping for {timeout} seconds.")
                time.sleep(timeout)

                backoff += 0.5
                continue
            else:
                break

        i += 1
        to_save.append(d)

        if new_doc["valid"]:
            new_doc = new_doc["output"]

            if not d.text: d.text = ""
            d.text += new_doc["text"] + " "

            d.features = None # Since the text was updated, re-initialise the features list
            d.stored_tweets = new_doc["stored_tweets"]
            d.first = new_doc["first"]
            d.last = new_doc["last"]
            print(f"User [{d.id}]: Retrieved {tweety.tweets_to_extract} tweets. ({(i % save_every)})")
        else:
            if d.text == "": d.text = None
            print(f"{new_doc['output']} ({i})")

        # Save the documents in `to_save` in batches of `save_every`
        if not(i % save_every) and len(to_save) != 0:
            db.session.bulk_save_objects(to_save)
            db.session.commit()
            print(f"=== Stored the documents of {i}/{N} users. ===")
            to_save = []

    if len(to_save) != 0:
        db.session.bulk_save_objects(to_save)
        db.session.commit()
        print(f"=== Stored the documents of {i}/{N} users. ===")

if __name__ == "__main__":
    manager.run()