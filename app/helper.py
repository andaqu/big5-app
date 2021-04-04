from models import personality, twitter
from .ext import db

schemas = {"twitter", "personality"}
required = {"twitter": ["id", "follows"], "personality": ["personality", "document"]}
document_model = {"twitter": twitter.Document, "personality": personality.Document}
user_model = {"twitter": twitter.User, "personality": personality.User}

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

def json(id, schema):
    user = user_model[schema].query.get_or_404(id)
    document = document_model[schema].query.get_or_404(id)
    
    response = {
        "_id": id,
        "user": user.json,
        "document" : document.json
    }
    return response