from flask_sqlalchemy import SQLAlchemy
from .ext import db

class Document(db.Model):
    __tablename__ = "Documents"

    id = db.Column(db.Integer, primary_key=True)
    document = db.Column(db.Text())

    def __init__(self, document):
        self.document = document

class User(db.Model):
    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key=True)
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