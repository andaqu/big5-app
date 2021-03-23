from models import personality, twitter
from .ext import db

schemas = {"twitter", "personality"}
required = {"twitter": ["id", "follows"], "personality": ["personality", "document"]}
document_model = {"twitter": twitter.Document, "personality": personality.Document}

def message(m, s="success"):
    return {"state" : s, "message": m}

def insert_to_personality(data):

    to_add = []

    for entry in data:
        p = entry["personality"]
        d = entry["document"]

        user = personality.User(personality=p)
        document = personality.Document(text=d)

        to_add.append(user)
        to_add.append(document)
        
    db.session.bulk_save_objects(to_add)
    db.session.commit()

def insert_to_twitter(data):

    to_add = []

    for entry in data:
        u = entry["id"]
        f = entry["follows"]

        user = twitter.User(id=u, follows=f)
        document = twitter.Document(id=u)

        to_add.append(user)
        to_add.append(document)
        
    db.session.bulk_save_objects(to_add)
    db.session.commit()

def retrieve_from_personality(id):
    user = personality.User.query.get_or_404(id)
    document = personality.Document.query.get_or_404(id)
    
    response = {
        "id": id,
        "personality": {
            "o" : user.o,
            "c" : user.c,
            "e" : user.e,
            "a" : user.a,
            "n" : user.n
        },
        "document" : {
            "_text" : document.text,
            "features" : document.features
        }
    }
    return response
    
def retrieve_from_twitter(id):
    user = twitter.User.query.get_or_404(id)
    document = twitter.Document.query.get_or_404(id)
    
    response = {
        "id": id,
        "follows": user.follows,
        "document" : {
            "_text" : document.text,
            "features" : document.features,
            "first" : document.first,
            "last" : document.last,
            "stored_tweets" : document.stored_tweets
        }
    }
    return response