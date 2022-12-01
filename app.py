from hashlib import new
from db import db
from flask import Flask
from db import User
from db import Group
from db import Post
import json
from flask import request
import os
import datetime
import users_dao
import bcrypt

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

def extract_token(request):
    """
    Helper function that extracts the token from the header of a request
    """
    auth_header = request.headers.get("Authorization")
    if auth_header is None:
        return False, failure_response("Missing authorization header.", 400)
    bearer_token = auth_header.replace("Bearer ", "").strip()
    if bearer_token is None or not bearer_token:
        return False, failure_response("Invalid authorization header.", 400)
    return True, bearer_token

# -- Landing Route __
@app.route("/")
def land():
    """
    Endpoint for landing page
    """
    return "Oasis"


# -- Authentication Routes --


# -- User Routes --
@app.route("/users/")
def get_users():
    """
    Endpoint for getting all users
    """
    users = [user.serialize()for user in User.query.all()]
    return success_response({"users": users})

@app.route("/users/register/", methods=["POST"])
def register_account():
    """
    Endpoint for registering a new user
    Authentication
    """
    body = json.loads(request.data)
    name = body.get("name")
    username = body.get("username")
    password = body.get("password")
    if name is None or username is None or password is None:
        return failure_response("Missing name, username or password.", 400)
    success, user = users_dao.create_user(name, username, password)
    if not success:
        return failure_response("User already exists.", 400)
    return success_response({
        "session_token": user.session_token,
        "session_expiration": str(user.session_expiration),
        "update_token": user.update_token
    })

@app.route("/users/login/", methods=["POST"])
def login():
    """
    Endpoint for logging in a user
    Authentication
    """
    body = json.loads(request.data)
    username = body.get("username")
    password = body.get("password")

    if username is None or password is None:
        return failure_response("Mising username or password!", 400)
    
    success, user = users_dao.verify_credentials(username,password)

    if not success:
        return failure_response("Incorrect username or password.", 401)

    return success_response({
        "session_token": user.session_token,
        "session_expiration": str(user.session_expiration),
        "update_token": user.update_token
    })

@app.route("/users/session/", methods=["POST"])
def update_session():
    """
    Endpoint for updating a user's session
    Authentication
    """
    success, update_token = extract_token(request)
    if not success:
        return failure_response("Could not extract session token", 400)
    success_user, user = users_dao.renew_session(update_token)
    if not success_user:
        return failure_response("Invalid update token", 400)
    return success_response({
        "session_token": user.session_token,
        "session_expiration": str(user.session_expiration),
        "update_token": user.update_token
    })

@app.route("/users/logout/", methods=["POST"])
def logout():
    """
    Endpoint for logging out a user
    """
    success, session_token = extract_token(request)

    if not success:
        return failure_response("Could not extract session token", 400)
    user = users_dao.get_user_by_session_token(session_token)
    if user is None or not user.verify_session_token(session_token):
        return failure_response("Invalid session token", 400)

    user.session_token = ""
    user.session_expiration = datetime.datetime.now()
    user.update_token = ""
    db.session.commit()

    return success_response({"message": "You have successfully logged out."})

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
    Authentication: Verifies session token and returns confirmation message
    """
    success, session_token = extract_token(request)
    if not success:
        return failure_response("Session token invalid", 400)
    user = users_dao.get_user_by_session_token(session_token)
    if user is None or not user.verify_session_token(session_token):
        return failure_response("Invalid session token", 400)
    body = json.loads(request.data)
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    new_name = body.get("name")
    if new_name is None:
        return failure_response("Must enter new name.", 400)
    user.name = new_name
    db.session.commit()
    return success_response({"message": "You have successfully updated your name!"})



@app.route("/users/<int:user_id>/username/", methods=["POST"])
def update_username(user_id):
    """
    Endpoint for updating username
    Authentication: Verifies session token and returns confirmation message
    """
    success, session_token = extract_token(request)
    if not success:
        return failure_response("Session token invalid", 400)
    user = users_dao.get_user_by_session_token(session_token)
    if user is None or not user.verify_session_token(session_token):
        return failure_response("Invalid session token", 400)
    body = json.loads(request.data)
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    new_username = body.get("username")
    if new_username is None:
        return failure_response("Must enter new username.", 400)
    user.username = new_username
    db.session.commit()
    return success_response({"message": "You have successfully updated your username!"})

# might need to change this
@app.route("/users/<int:user_id>/password/", methods=["POST"])
def update_password(user_id):
    """
    Endpoint for updating password
    Authentication: Verifies session token and returns confirmation message
    """
    success, session_token = extract_token(request)
    if not success:
        return failure_response("Session token invalid", 400)
    user = users_dao.get_user_by_session_token(session_token)
    if user is None or not user.verify_session_token(session_token):
        return failure_response("Invalid session token", 400)
    body = json.loads(request.data)
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    new_password = body.get("password")
    if new_password is None:
        return failure_response("Must enter new password.", 400)
    user.password_digest = bcrypt.hashpw(new_password.encode("utf8"), bcrypt.gensalt(rounds=13))
    db.session.commit()
    return success_response({"message": "You have successfully updated your password!"})

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
        return failure_response("Group not found!")
    user = User.query.filter_by(id=(body.get("user_id"))).first()
    if user is None:
        return failure_response("User not found!")

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
        return failure_response("Group not found!")
    user = User.query.filter_by(id=(body.get("user_id"))).first()
    if user is None:
        return failure_response("User not found!")
    group.users.remove(user)
    db.session.commit()
    return success_response(group.serialize())

# -- Post Routes --
@app.route("/groups/<int:group_id>/posts/")
def get_posts(group_id):
    """
    Endpoint for getting all posts in a specific group
    """
    group = Group.query.filter_by(id=group_id).first()
    if group is None:
        return failure_response("Group not found!")
    return success_response(group.post_serialize())

@app.route("/users/<int:user_id>/posts/", methods=["POST"])
def create_post(user_id):
    """
    Endpoint for creating a post for a user
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    body = json.loads(request.data)
    new_post = Post(title = body.get("title"), timestamp = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S%.%M"), message = body.get("message"), user_id=user_id)
    if new_post.title is None or new_post.message is None:
        return failure_response("Must enter title and message.", 400)
    db.session.add(new_post)
    user.posts.append(new_post)
    db.session.commit()
    return success_response(new_post.serialize(), 201)

@app.route("/users/<int:user_id>/posts/<int:post_id>/")
def get_post(user_id, post_id):
    """
    Endpoint for getting a user's post by id
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        return failure_response("Post not found!")
    return success_response(post.serialize())

@app.route("/users/<int:user_id>/posts/<int:post_id>/", methods=["DELETE"])
def delete_post(user_id, post_id):
    """
    Endpoint for deleting user's post
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        return failure_response("Post not found!")
    db.session.delete(post)
    db.session.commit()
    return success_response(post.simple_serialize())

    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)