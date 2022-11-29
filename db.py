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
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, nullable = False)
    username = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    groups = db.relationship("Group", secondary = association_table, back_populates = "users")

    def __init__(self, **kwargs):
        """
        Creates User object
        """
        self.name = kwargs.get("name", "")
        self.username = kwargs.get("username", "")
        self.password = kwargs.get("password", "")

    def serialize(self):
        """
        Serializes a User object
        """
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "groups": [g.simple_serialize() for g in self.groups] 
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
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    users = db.relationship("User", secondary=association_table, back_populates='groups')

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

    def simple_serialize(self):
        """
        Simple serializes a Group object
        """
        return {
            "id": self.id,
            "name": self.name
        }
