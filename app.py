from hashlib import new
from db import db
from flask import Flask
from db import User
from db import Group
import json
from flask import request
import os

app = Flask(__name__)
db_filename = "cms.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

# generalized response formats
def success_response(data, code=200):
    return json.dumps(data), code

def failure_response(message, code=404):
    return json.dumps({"error":message}), code

# -- Landing Route __
@app.route("/")
def land():
    """
    Endpoint for landing page
    """
    return "Oasis"


# -- User Routes --
@app.route("/users/")
def get_users():
    """
    Endpoint for getting all users
    """
    users = [user.serialize()for user in User.query.all()]
    return success_response({"users": users})

@app.route("/users/", methods=["POST"])
def create_user():
    """
    Endpoint for creating a new user
    """
    body = json.loads(request.data)
    new_user = User(name = body.get("name"), username = body.get("username"), password = body.get("password"))
    if new_user.name is None or new_user.username is None or new_user.password is None: 
        return failure_response("Must enter name, username, and password.", 400)
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(), 201)

@app.route("/users/<int:user_id>/")
def get_user(user_id):
    """
    Endpoint for getting a user by id
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    return success_response(user.serialize())

@app.route("/users/<int:user_id>/name/", methods=["POST"])
def update_name(user_id):
    """
    Endpoint for updating a user's name
    """
    body = json.loads(request.data)
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    new_name = body.get("name")
    if new_name is None:
        return failure_response("Must enter new name.", 400)
    user.name = new_name
    db.session.commit()
    return success_response(user.simple_serialize())

@app.route("/users/<int:user_id>/username/", methods=["POST"])
def update_username(user_id):
    """
    Endpoint for updating username
    """
    body = json.loads(request.data)
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    new_username = body.get("username")
    if new_username is None:
        return failure_response("Must enter new username.", 400)
    user.username = new_username
    db.session.commit()
    return success_response(user.simple_serialize())

@app.route("/users/<int:user_id>/password/", methods=["POST"])
def update_password(user_id):
    """
    Endpoint for updating password
    """
    body = json.loads(request.data)
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    new_password = body.get("password")
    if new_password is None:
        return failure_response("Must enter new password.", 400)
    user.password = new_password
    db.session.commit()
    return success_response(user.simple_serialize()) # might wannt replace with text

@app.route("/users/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    """
    Endpoint for deleting a user by id
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    db.session.delete(user)
    db.session.commit()
    return success_response(user.serialize())

# -- Group Routes --
@app.route("/groups/")
def get_groups():
    """
    Endpoint for getting all groups
    """
    groups = [group.simple_serialize()for group in Group.query.all()]
    return success_response({"groups": groups})

@app.route("/groups/", methods=["POST"])
def create_group():
    """
    Endpoint for creating a new group
    """
    body = json.loads(request.data)
    new_group = Group(name = body.get("name"))
    if new_group.name is None: 
        return failure_response("Must enter group name", 400)
    db.session.add(new_group)
    db.session.commit()
    return success_response(new_group.simple_serialize(), 201)

@app.route("/groups/<int:group_id>/")
def get_group(group_id):
    """
    Endpoint for getting a group by id
    """
    group = Group.query.filter_by(id=group_id).first()
    if group is None:
        return failure_response("Group not found!")
    return success_response(group.serialize())

@app.route("/groups/<int:group_id>/", methods=["DELETE"])
def delete_group(group_id):
    """
    Endpoint for deleting a group by id
    """
    group = Group.query.filter_by(id=group_id).first()
    if group is None:
        return failure_response("Group not found!")
    db.session.delete(group)
    db.session.commit()
    return success_response(group.serialize())

@app.route("/groups/<int:group_id>/name/", methods=["POST"])
def update_group_name(group_id):
    """
    Endpoint for updating a group's name
    """
    body = json.loads(request.data)
    group = Group.query.filter_by(id=group_id).first()
    if group is None:
        return failure_response("Group not found!")
    new_name = body.get("name")
    if new_name is None:
        return failure_response("Must enter new name.", 400)
    group.name = new_name
    db.session.commit()
    return success_response(group.simple_serialize())

@app.route("/groups/<int:group_id>/add/", methods=["POST"])
def add_user_to_group(group_id):
    """
    Endpoint for adding a user to a group
    """
    body = json.loads(request.data)
    group = Group.query.filter_by(id=group_id).first()
    if group is None:
        return failure_response("Group does not exist.")
    user = User.query.filter_by(id=(body.get("user_id"))).first()
    if user is None:
        return failure_response("User does not exist.")

    group.users.append(user)
    user.groups.append(group)
    db.session.commit()
    return success_response(group.serialize())

@app.route("/groups/<int:group_id>/remove/", methods=["POST"])
def remove_user_from_group(group_id):
    """
    Endpoint for removing a user from a group
    """
    body = json.loads(request.data)
    group = Group.query.filter_by(id=group_id).first()
    if group is None:
        return failure_response("Group does not exist.")
    user = User.query.filter_by(id=(body.get("user_id"))).first()
    if user is None:
        return failure_response("User does not exist.")
    
    group.users.remove(user)
    db.session.commit()
    return success_response(group.serialize())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)