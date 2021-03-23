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

class User(BaseUser, db.Model):
    __table_args__ = {'schema': "twitter"}
    __tablename__ = "User"

    id = db.Column(db.String, primary_key=True)
    follows = db.Column(db.ARRAY(db.String()))

    def __init__(self, id, follows):
        self.id = id
        self.follows = follows