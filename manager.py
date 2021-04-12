from app import create_app, db, base, twitter, document_model, user_model
from personality_recogniser import Recogniser
from sqlalchemy import create_engine
from itertools import zip_longest
from flask_migrate import Manager
from bot import Tweety
import pandas as pd
import time

app = create_app()
manager = Manager(app)
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])

@manager.option("-s", "--schema", dest="s", help="Schema to featurise documents of.", default="personality")
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

    LIMIT = b
    OFFSET = 0

    # Get documents which have text
    docs = db.session.query(Document).filter(Document.text != "").filter(Document.text != None).limit(LIMIT).offset(OFFSET).all()

    # Get documents which have text but are not featurised
    # docs = db.session.query(Document).filter(Document.features == None).filter(Document.text != "").filter(Document.text != None).limit(LIMIT).offset(OFFSET).all()

    N = db.session.query(Document).filter(Document.text != "").filter(Document.text != None).count()

    if N == 0:
        print("No documents to featurise.")
        return

    print(f"Featurising [{N}] documents from [{s}] schema and saving every [{b}] documents...")
    
    i = 0

    t0 = time.time()

    while len(docs) > 0:

        for d in docs:
            d.compute_features()
            i += 1

        db.session.bulk_save_objects(docs)
        db.session.commit()
        print(f"*** Featurised and saved {i}/{N} documents. ***")
        
        OFFSET += LIMIT
        docs = db.session.query(Document).filter(Document.text != "").filter(Document.text != None).limit(LIMIT).offset(OFFSET).all()

    t1 = time.time()

    print(f"Done! That took {(t1-t0)/60} minutes in total.")

# worker: python manager.py get_tweets -n 400 -b 200 -f
@manager.option("-n", "--tweets", dest="n", help="Number of tweets to extract from every user.", default=400)
@manager.option("-b", "--batch_size", dest="b", help="Batch size to commit to database.", default=100)
@manager.option("-f", "--force_all", dest="f", help="Retrieve tweets of every user in database (restarting the process)", default=True)
def get_tweets(n, b, f):

    # Check if parameters are valid
    try:
        n = int(n)
        b = int(b)
        f = bool(int(f))
    except:
        print("Revise parameters. Quitting...")
        return

    # Check if table "Document" exists within the specified schema
    if not engine.dialect.has_table(engine, "Document", schema="twitter"):
        print(f"Table 'twitter.Document' does not exist. Migrate and try again.")
        return

    # Initialise Tweety
    tweety = Tweety(tweets_to_extract=n)

    print(f"Force-all mode: {'enabled' if f else 'disabled'}")

    if f:
        # If the --force_all mode is enabled, every user will have their 'document' updated
        # (Due to memory limitations, they will be extracted in batches)
        N = db.session.query(twitter.Document).count()

        LIMIT = b
        OFFSET = 0
        docs = db.session.query(twitter.Document).limit(LIMIT).offset(OFFSET).all()

        i = 0

        while len(docs) > 0:
            i = update_documents(tweety, docs, N, save_every=b, i=i)
            OFFSET += LIMIT
            docs = db.session.query(twitter.Document).limit(LIMIT).offset(OFFSET).all()
    else:
        # Get document rows which have an empty text field and order them by ID
        docs = db.session.query(twitter.Document).filter(twitter.Document.text == "").order_by(twitter.Document.id).all()
        N = len(docs)

        if N == 0:
            print("All of the users have a filled-in text field. Set the --force_all parameter to True to consider all users. Quitting...")
            return

        update_documents(tweety, docs, N, save_every=b)

    return

def update_documents(tweety:Tweety, docs, N:int, save_every:int, i:int=0):
    """
    :tweety: Tweety instance
    :docs: List of documents from Document table
    :N: Total length of Document table
    :save_every: Add to database in batches of save_every
    """ 
    to_save = []

    for d in docs:

        backoff = 0.1

        # tweety.get_document is covered in an infinite loop in the cases where the bot requires us to sleep due to an
        # interrupted / disallowed connection (not talking about rate limits here), sleeping for `backoff` and trying
        # the retrieving the same document again after a backoff period.
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
            print(f"User [{d.id}]: Retrieved {tweety.tweets_to_extract} tweets. ({i})")
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

    return i

@manager.option("-b", "--batch_size", dest="b", help="Batch size to personalise and commit to database.", default=5000)
@manager.option("-f", "--force_all", dest="f", help="Whether to personalise all of the users.", default=False)
def personalise(b, f):

    # Check if parameters are valid
    try:
        b = int(b)
    except:
        print("Revise parameters. Quitting...")
        return

    # Check if table "Document" and "User" exist within the specified schema
    if not (engine.dialect.has_table(engine, "Document", schema="twitter") and engine.dialect.has_table(engine, "User", schema="twitter")):
        print(f"Table 'twitter.Document' and/or 'twitter.User' do not exist. Migrate and try again.")
        return

    print(f"Force-all mode: {'enabled' if f else 'disabled'}")

    Document = document_model["twitter"]
    User = user_model["twitter"]

    if f:
        # Get users to personalise which have a filled-in features field.
        result = db.session.query(Document, User).filter(Document.id == User.id).filter(Document.features != None).all()
    else:
        # Get users to personalise which have a filled-in features field and do not have a personality.
        result = db.session.query(Document, User).filter(Document.id == User.id).filter(Document.features != None).filter(User.o == None).all()

    N = len(result)

    if N == 0:
        print("No users to personalise. Check if the users' documents are featurised or try including the --force_all parameter.")
        return

    print(f"Extracting personality from [{N}] twitter users and saving every [{b}] users...")

    # Initialise recogniser with a list of feature names.
    features = [column.name for column in base.Word.__table__.columns][1:]
    recogniser = Recogniser(features)

    i = 0

    t0 = time.time()

    for res in chunks(result, b):
        documents, users = zip(*res)
        
        X = { d.id : d.features for d in documents } # TODO: Have a look if this can be optimised

        y = recogniser.personalise(X)
        if not y: break

        for u in users:
            u.o = y[u.id]["o"]
            u.c = y[u.id]["c"]
            u.e = y[u.id]["e"]
            u.a = y[u.id]["a"]
            u.n = y[u.id]["n"]

        if i + b > N:
            i += len(users)
        else:
            i += b

        db.session.bulk_save_objects(users)
        db.session.commit()
        print(f"=== Recognised and stored the personality of {i}/{N} users. ===")

    t1 = time.time()
    print(f"Done! That took {(t1-t0)/60} minutes in total.")

    return

def chunks(lst, n):
    """
    Yield successive n-sized chunks from lst.
    """
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

if __name__ == "__main__":
    manager.run()