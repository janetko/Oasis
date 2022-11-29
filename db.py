from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Association Tables
association_table = db.Table (
    # Many to Many
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
    groups = db.relationship("group", secondary = association_table, back_populates = "users")

    def __init__(self, **kwargs):
        """
        Creates user object
        """
        self.name = kwargs.get("name", "")
        self.username = kwargs.get("username", "")
        self.password = kwargs.get("password", "")

    def serialize(self):
        """
        serializes a user object
        """
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "groups": [g.serialize() for g in self.groups] # serialize or simple serialize
        }

    def simple_serialize(self):
        """
        simple serializes a user object
        """
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username
        }

# -- Group Class --
class Group(db.Model):
    __tablename__ = "group"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)
    users = db.relationship("user", secondary=association_table, back_populates='groups')

    def serialize(self):
        return {
            "id": self.id,
            "type": self.description,
        }
