from models.base import BaseDocument, BaseUser
from app.ext import db

class Document(BaseDocument, db.Model):
    __table_args__ = {'schema': "twitter"}
    __tablename__ = "Document"

class User(BaseUser, db.Model):
    __table_args__ = {'schema': "twitter"}
    __tablename__ = "User"

    total = db.Column(db.Integer())
    first = db.Column(db.Integer())
    last = db.Column(db.Integer())
    
    def __init__(self, id, total, first, last):
        self.id = id
        self.total = total
        self.first = first
        self.last = last
