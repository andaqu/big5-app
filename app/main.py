from flask import Blueprint, request
from .helper import *
from .ext import *

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return f"<h>Server is running</h>"  

# Retrieves or deletes a user-document entry from database
@main.route("/<schema>/<id>", methods=["GET"])
def retrieve(schema, id):

    if request.method != "GET":
        return message("The request is not a GET request.", s="error")

    if schema not in schemas:
        return message("Specified schema is not valid.", s="error")

    return json(id, schema)
