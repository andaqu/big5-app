import os

SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL").replace(":/", "ql:/")
SQLALCHEMY_TRACK_MODIFICATIONS = False