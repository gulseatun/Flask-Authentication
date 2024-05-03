from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'cdefghjklm'

    # Configure the database URI for SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_NAME

    # Initialize the SQLAlchemy database with the Flask application
    db.init_app(app)

    # Import blueprints for different parts of the application
    from .views import views
    from .auth import auth

    # Register the blueprints with the application and define URL prefixes
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    # Create the database if it doesn't exist
    create_database(app)

    # Configure Flask-Login for user session management
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Define a user loader function for Flask-Login to load users from the database
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app


# Function to create the database
def create_database(app):
    # Use the application context to perform database operations
    with app.app_context():
        # Check if the database file exists
        if not path.exists("website/" + DB_NAME):
            # Create all database tables based on defined models
            db.create_all()
