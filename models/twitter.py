from models.base import BaseDocument, BaseUser
from app.ext import db

class Document(BaseDocument, db.Model):
    __table_args__ = {'schema': "twitter"}
    __tablename__ = "Document"

    stored_tweets = db.Column(db.Integer())
    first = db.Column(db.Numeric())
    last = db.Column(db.Numeric())

    def __init__(self, id):
        self.id = id
        self.text = ""
        self.stored_tweets = None
        self.first = None
        self.last = None

    @property
    def json(self):
        return {
            "text": self.text,
            "features": self.features,
            "stored_tweets": self.stored_tweets,
            "first": self.first,
            "last": self.last
        }

class User(BaseUser, db.Model):
    __table_args__ = {'schema': "twitter"}
    __tablename__ = "User"

    follows = db.Column(db.ARRAY(db.Integer()))

    def __init__(self, id, follows):
        self.id = id
        self.follows = follows

    @property
    def json(self):
        return {
            "follows": self.follows,
            "personality": { "o": self.o, "c": self.c, "e": self.e, "a": self.a, "n": self.n }
        }