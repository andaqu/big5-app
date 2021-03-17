from flask import Blueprint, request
from sqlalchemy import func
from .models import *
from .ext import *

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return f"<h>Server is running</h>"

# Takes a list of user-document entries and adds them to database
# If alongside such entries, an identifier is given, then the entry with that identifier is edited
#? This was found to be the better approach than sending continuous post requests, creating a very-slow overhead
@main.route("/populate", methods=["POST"])
def populate():
    # Check if request is a POST request
    if request.method == "POST":

        # It is assumed that data is sent as JSON
        data = request.get_json()
        
        # Data must be a list to process request
        if type(data) is not list:
            return message("The request payload is not a list.", s="error")

        # Check that every entry contains personality or document keys before processing
        for entry in data:
            if "personality" not in entry or "document" not in entry:
                return message("The request payload does not contain personality and document.", s="error")

        # Process requests
        for entry in data:
            p = entry["personality"]
            d = entry["document"]

            user = User(o=p['o'], c=p['c'], e=p['e'], a=p['a'], n=p['n'])
            document = Document(text=d)

            db.session.add(user)
            db.session.add(document)

            db.session.commit()

        return message("User has been added or updated successfully.")
    else:
        return message("The request is not a POST request.", s="error")

# Retrieves or deletes a user-document entry from database
@main.route("/user/<id>", methods=["GET"])
def retrieve(id):
    user = User.query.get_or_404(id)
    document = Document.query.get_or_404(id)

    if request.method == "GET":
        response = {
            "id": id,
            "personality": {
                "o" : user.o,
                "c" : user.c,
                "e" : user.e,
                "a" : user.a,
                "n" : user.n
            },
            "document" : {
                "_text" : document.text,
                "features" : document.features
            }
        }
        return message(response)

def message(m, s="success"):
    return {"state" : s, "message": m}
