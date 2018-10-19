
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()


class User(UserMixin, db.Model):

    id = db.Column(db.Integer,primary_key=True, autoincrement=True )
    username = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(130), nullable=False)
    icons = db.Column(db.String(130), nullable=True)

    __tablename__ = 'user'