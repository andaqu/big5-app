from models.base import BaseDocument, BaseUser
from app.ext import db

class Document(BaseDocument, db.Model):
    __table_args__ = {'schema': "personality"}
    __tablename__ = "Document"

class User(BaseUser, db.Model):
    __table_args__ = {'schema': "personality"}
    __tablename__ = "User"

    o = db.Column(db.Float())
    c = db.Column(db.Float())
    e = db.Column(db.Float())
    a = db.Column(db.Float())
    n = db.Column(db.Float())

    def __init__(self, o, c, e, a, n):
        self.o = o
        self.c = c
        self.e = e
        self.a = a
        self.n = n
