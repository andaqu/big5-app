from flask import Blueprint
from flask import request
from .models import *

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return f"<h>Server is running</h>"

# Adds a user to the database
@main.route("/add", methods=["POST"])
def add_entry():
    if request.method == 'POST':
        if request.is_json:

            data = request.get_json()

            user = User(o=data['o'], c=data['c'], e=data['e'], a=data['a'], n=data['n'])
            document = Document(document=data['document'])

            db.session.add(user)
            db.session.add(document)

            db.session.commit()

            return {"message": f"User has been added successfully."}
        else:
            return {"error": "The request payload is not in JSON format."}
    else:
        return {"error" : "The request is not a POST request."}