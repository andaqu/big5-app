from flask import Blueprint
from flask import request
from .models import *

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return f"<h>Server is running</h>"

# Adds a singular user-document pair to database
@main.route("/add", methods=["POST"])
def add_pair():
    if request.method == "POST":
        if request.is_json:

            data = request.get_json()

            try: 
                add(data["personality"], data["document"])
            except KeyError: 
                return {"state" : "error", "message": "The request payload does not contain personality and document."}

            return {"state" : "success", "message": f"User has been added successfully."}
        else:
            return {"state" : "error", "message": "The request payload is not in JSON format."}
    else:
        return {"state" : "error", "message": "The request is not a POST request."}

def add(p, d):
    user = User(o=p['o'], c=p['c'], e=p['e'], a=p['a'], n=p['n'])
    document = Document(text=d)

    db.session.add(user)
    db.session.add(document)

    db.session.commit()

# Retrieve, edit or delete a user-document pair from database
@main.route('/user/<id>', methods=['GET', 'PUT', 'DELETE'])
def handle_pair(id):
    user = User.query.get_or_404(id)
    document = Document.query.get_or_404(id)

    if request.method == 'GET':
        response = {
            "id": user.id,
            "o" : user.o,
            "c" : user.c,
            "e" : user.e,
            "a" : user.a,
            "n" : user.n,
            "document" : document.text
        }
        return {"state": "success", "message": response}

    elif request.method == 'PUT':
        data = request.get_json()

        user.o = data["personality"]["o"]
        user.c = data["personality"]["c"]
        user.e = data["personality"]["e"]
        user.a = data["personality"]["a"]
        user.n = data["personality"]["n"]
        document.text = data["document"]

        db.session.add(user)
        db.session.add(document)
        db.session.commit()

        return {"state": "success", "message": f"User {user.id} successfully updated."}

    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.delete(document)
        db.session.commit()
        return {"state": "success", "message": f"User {user.id} successfully deleted."}