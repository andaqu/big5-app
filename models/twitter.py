from models.base import BaseDocument, BaseUser
from app.ext import db

class Document(BaseDocument, db.Model):
    __table_args__ = {'schema': "twitter"}
    __tablename__ = "Document"

class User(BaseUser, db.Model):
    __table_args__ = {'schema': "twitter"}
    __tablename__ = "User"

    first = db.Column(db.Integer())
    last = db.Column(db.Integer())

    def __init__(self, id, first, last):
        self.id = id
        self.first = first
        self.last = last
