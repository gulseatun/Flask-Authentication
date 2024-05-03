from flask import Blueprint, render_template, request, flash, url_for, redirect
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, login_required, current_user

# Create a blueprint named 'auth'
auth = Blueprint('auth', __name__)


# Route for signing in
@auth.route('/', methods=['GET', 'POST'])
def sign_in():
    # Check if the user is already logged in
    if current_user.is_authenticated:
        # If the user is logged in, redirect to the logout page
        return redirect(url_for('auth.logout'))

    # If the request method is POST, process form submission
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        # Query the database for the user with the provided email
        user = User.query.filter_by(email=email).first()
        if user:
            # If the user exists, check the password hash
            if check_password_hash(user.password, password):
                # If the password is correct, log the user in
                flash('Welcome back!', 'success')
                login_user(user, remember=True)
                print('Logged in successfully!')
                # Redirect the user to the logout page
                return redirect(url_for('auth.logout'))
            else:
                # If the password is incorrect, show an error message
                flash('Incorrect Password', 'error')
        else:
            # If the user does not exist, show an error message
            flash("User does not exist", 'error')

    # Render the sign-in template with the current user
    return render_template("sign_in.html", user=current_user)

# Route for signing up
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    # If the request method is POST, process form submission
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password-confirm')

        # Check if the user already exists
        user = User.query.filter_by(email=email).first()
        # If the user does not exist, validate the form data
        if not user:
            if len(email) <4:
                flash("Please enter a valid email address.", category="error")

            elif password != password2:
                flash("Passwords must match.", category="error")

            elif len(password) < 8:
                flash("Password must be at least 8 characters.", category="error")

            # If the form data is valid, create a new user
            else:
                new_user = User(email=email, password=generate_password_hash(password, method='pbkdf2:sha256'))
                db.session.add(new_user)
                db.session.commit()
                # Log the new user in and show a success message
                login_user(new_user, remember=True)
                flash("You have successfully registered.", category="success")
                # Redirect the user to the logout page
                return redirect(url_for('auth.logout'))

        else:
            # If the user already exists, show an error message
            flash("User already exists.", category="error")

    # Render the sign-up template with the current user
    return render_template("sign_up.html", user=current_user)


# Route for logging out
@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    # If the request method is POST, log the user out and redirect to the sign-in page
    if request.method == 'POST':
        logout_user()
        return redirect(url_for('auth.sign_in'))

    # If the request method is GET, render the logout template
    else:
        return render_template("logout.html", user=current_user)
