from flask import Blueprint
from flask import request
from .models import *

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return f"<h>Server is running</h>"

# Adds user-document pair to database
@main.route("/add", methods=["POST"])
def add_pair():
    if request.method == 'POST':
        if request.is_json:

            data = request.get_json()

            user = User(o=data['o'], c=data['c'], e=data['e'], a=data['a'], n=data['n'])
            document = Document(text=data['document'])

            db.session.add(user)
            db.session.add(document)

            db.session.commit()

            return {"message": f"User has been added successfully."}

        else:
            return {"error": "The request payload is not in JSON format."}
    else:
        return {"error" : "The request is not a POST request."}

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
        return {"message": "success", "response": response}

    elif request.method == 'PUT':
        data = request.get_json()

        user.o = data['o']
        user.c = data['c']
        user.e = data['e']
        user.a = data['a']
        user.n = data['n']
        document.text = data['document']

        db.session.add(user)
        db.session.add(document)
        db.session.commit()

        return {"message": f"User {user.id} successfully updated."}

    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.delete(document)
        db.session.commit()
        return {"message": f"User {user.id} successfully deleted."}