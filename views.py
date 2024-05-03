from flask import Blueprint, render_template
from flask_login import current_user, login_required

views = Blueprint('views', __name__)

@views.route('/logout')
@login_required
def logout():
    return render_template("logout.html", user=current_user)