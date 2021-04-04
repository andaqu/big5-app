from flask import Blueprint, request
from .helper import *
from .ext import *

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return f"<h>Server is running</h>"

# Takes a list of user-document entries and adds them to database
# If alongside such entries, an identifier is given, then the entry with that identifier is edited
#? This was found to be the better approach than sending continuous post requests, creating a very-slow overhead
@main.route("/<schema>/populate", methods=["POST"])
def populate(schema):

    # Check if request is a POST request
    if request.method != "POST":
        return message("The request is not a POST request.", s="error")

    # Check if schema is valid
    if schema not in schemas:
        return message("Specified schema is not valid.", s="error")

    # It is assumed that data is sent as JSON
    data = request.get_json()
    
    # Data must be a list to process request
    if type(data) is not list:
        return message("The request payload is not a list.", s="error")

    # Check that every entry contains the required keys before processing
    for entry in data:
        if not all(x in required[schema] for x in entry):
            return message("The request payload contains invalid and/or missing keys.", s="error")

    if schema == "twitter": insert_to_twitter(data)
    elif schema == "personality": insert_to_personality(data)

    return message(f"Population of {len(data)} objects completed successfully.")
        

# Retrieves or deletes a user-document entry from database
@main.route("/<schema>/<id>", methods=["GET"])
def retrieve(schema, id):

    if request.method != "GET":
        return message("The request is not a GET request.", s="error")

    if schema not in schemas:
        return message("Specified schema is not valid.", s="error")

    return json(id, schema)
