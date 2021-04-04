from models.base import BaseDocument, BaseUser
from app.ext import db

class Document(BaseDocument, db.Model):
    __table_args__ = {'schema': "personality"}
    __tablename__ = "Document"

class User(BaseUser, db.Model):
    __table_args__ = {'schema': "personality"}
    __tablename__ = "User"
    
    def __init__(self, personality):

        self.o = personality["o"]
        self.c = personality["c"]
        self.e = personality["e"]
        self.a = personality["a"]
        self.n = personality["n"]