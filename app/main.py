from flask import Blueprint
from flask import request
from .models import *

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
            return error("The request payload is not a list.")

        # Check every entry contains personality or document keys before processing
        for entry in data:
            if "personality" not in entry or "document" not in entry:
                return error("The request payload does not contain personality and document.")

        # Process requests
        for entry in data:
            add_or_update(entry)

        return {"state" : "success", "message": "User has been added or updated successfully."}
    else:
        return error("The request is not a POST request.")

# Retrieves or deletes a user-document entry from database
@main.route("/user/<id>", methods=["GET", "DELETE"])
def handle(id):

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
            "document" : document.text
        }
        return {"state": "success", "message": response}

    elif request.method == "DELETE":
        db.session.delete(user)
        db.session.delete(document)
        db.session.commit()
        return {"state": "success", "message": f"User {user.id} successfully deleted."}

def error(m):
    return {"state" : "error", "message": m}

def add_or_update(entry):

    p = entry["personality"]
    d = entry["document"]

    # If id is not within entry, then it is an append operation
    if "id" not in entry:
        user = User(o=p['o'], c=p['c'], e=p['e'], a=p['a'], n=p['n'])
        document = Document(text=d)

    # Otherwise it's an update operation
    else:
        user = User.query.get_or_404(entry["id"])
        document = Document.query.get_or_404(entry["id"])

        user.o = p['o']
        user.c = p['c']
        user.e = p['e']
        user.a = p['a']
        user.n = p['n']

        document.text = d

    db.session.add(user)
    db.session.add(document)

    db.session.commit()