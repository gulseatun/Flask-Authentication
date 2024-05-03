from . import db
from flask_login import UserMixin


# Define the User model class, which inherits from db.Model and UserMixin
class User(db.Model, UserMixin):
    # Define the database columns for the User model
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
