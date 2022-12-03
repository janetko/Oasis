import datetime
import hashlib
import os
import bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Association Tables
association_table = db.Table (
    # Many to Many
    "association",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("group_id", db.Integer, db.ForeignKey("group.id"))
)

# -- User Class --
class User(db.Model):
    """
    User model
    many to many relationship with Group
    one to many relationshiop with Post
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    # User information
    name = db.Column(db.String, nullable = False)
    username = db.Column(db.String, nullable = False)
    password_digest = db.Column(db.String, nullable = False)
    groups = db.relationship("Group", secondary = association_table, back_populates = "users")
    posts = db.relationship("Post", cascade = "delete")

    # Session information
    session_token = db.Column(db.String, nullable = False, unique = True)
    session_expiration = db.Column(db.DateTime, nullable = False)
    update_token = db.Column(db.String, nullable = False, unique = True)

    def __init__(self, **kwargs):
        """
        Creates User object
        """
        self.name = kwargs.get("name", "")
        self.username = kwargs.get("username", "")
        self.password_digest = bcrypt.hashpw(kwargs.get("password").encode("utf8"), bcrypt.gensalt(rounds=13))
        self.renew_session()

    def _urlsafe_base_64(self):
        """
        Randomly generates hashed tokens (used for session/update tokens)
        """
        return hashlib.sha1(os.urandom(64)).hexdigest()

    def renew_session(self):
        """
        Renews the sessions, i.e.
        1. Creates a new session token
        2. Sets the expiration time of the session to be a day from now
        3. Creates a new update token
        """
        self.session_token = self._urlsafe_base_64()
        self.session_expiration = datetime.datetime.now() + datetime.timedelta(days=1)
        self.update_token = self._urlsafe_base_64()

    def verify_password(self, password):
        """
        Verifies the password of a user
        """
        return bcrypt.checkpw(password.encode("utf8"), self.password_digest)

    def verify_session_token(self, session_token):
        """
        Verifies the session token of a user
        """
        return session_token == self.session_token and datetime.datetime.now() < self.session_expiration

    def verify_update_token(self, update_token):
        """
        Verifies the update token of a user
        """
        return update_token == self.update_token

    def pass_serialize(self):
        """
        Serializes a User object with password
        """
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "password": str(self.password_digest),
            "groups": [g.simple_serialize() for g in self.groups],
            "posts": [p.simple_serialize() for p in self.posts]
        }

    def serialize(self):
        """
        Serializes a User object
        """
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "groups": [g.simple_serialize() for g in self.groups],
            "posts": [p.simple_serialize() for p in self.posts]
        }

    def simple_serialize(self):
        """
        Simple serializes a User object
        """
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username
        }

# -- Group Class --
class Group(db.Model):
    """
    Group model
    many to many relationship with User
    """
    __tablename__ = "group"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, nullable = False)
    users = db.relationship("User", secondary = association_table, back_populates = 'groups')

    def __init__(self, **kwargs):
        """
        Creates Group object
        """
        self.name = kwargs.get("name", "")

    def serialize(self):
        """
        Serializes a Group object
        """
        return {
            "id": self.id,
            "name": self.name,
            "users": [u.simple_serialize() for u in self.users]
        }


    def post_serialize(self):
        """
        Serializes a Group object with its posts
        """
        posts = []
        for user in self.users:
            for post in user.posts:
                posts.append(post)

        return {
            "id": self.id,
            "name": self.name,
            "posts": [p.serialize() for p in posts]
        }

    def simple_serialize(self):
        """
        Simple serializes a Group object
        """
        return {
            "id": self.id,
            "name": self.name
        }

# -- Post Class --
class Post(db.Model):
    """
    Post model
    many to one relationship with User
    """
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String, nullable = False)
    timestamp = db.Column(db.Integer, nullable = False)
    message = db.Column(db.String, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User")

    def __init__(self, **kwargs):
        """
        Creates a Post object
        """
        self.title = kwargs.get("title", "")
        self.timestamp = kwargs.get("timestamp", "")
        self.message = kwargs.get("message", "")
        self.user_id = kwargs.get("user_id")

    def serialize(self):
        """
        Serializes a Post object
        """
        return {
            "id": self.id,
            "title": self.title,
            "timestamp": self.timestamp,
            "message": self.message,
            "user": self.user.simple_serialize()
        }

    def simple_serialize(self):
        """
        Simple serializes a Post object
        """
        return {
            "id": self.id,
            "title": self.title,
            "timesamp": self.timestamp,
            "message": self.message
        }


