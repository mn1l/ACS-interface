from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template('home.html')

@views.route('/index')
@login_required
def index():
    return render_template('index.html', user=current_user)

@views.route('/feedback')
def feedback():
    return render_template('feedback.html')