
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(255))
    username = db.Column(db.String(80))

    def __init__(self, body, username):
        self.body = body
        self.username = username

# You can add other models and database configurations if needed
