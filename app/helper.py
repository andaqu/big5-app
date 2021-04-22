from models import personality, twitter, base
from .ext import db

schemas = {"twitter", "personality"}
required = {"twitter": ["id", "follows"], "personality": ["personality", "document"]}
document_model = {"twitter": twitter.Document, "personality": personality.Document}
user_model = {"twitter": twitter.User, "personality": personality.User}
features = base.WORDF_NAMES

def message(m, s="success"):
    return {"state" : s, "message": m}

def json(id, schema):
    user = user_model[schema].query.get_or_404(id)
    document = document_model[schema].query.get_or_404(id)
    
    response = {
        "_id": id,
        "user": user.json,
        "document" : document.json
    }
    return response