from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from . import db
from .models import Data

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template('home.html')

@views.route('/index')
@login_required
def index():
    # hier

    data = Data.query.order_by(Data.id.desc()).first()

    return render_template(
        'dashboard.html', 
        user=current_user,
        luchttemp=f"{data.luchttemp:.2f}",
        luchtdruk=f"{data.luchtdruk:.2f}",
        luchtvochtigheid=f"{data.luchtvochtigheid:.2f}",
    )

@views.route('/feedback')
@login_required
def feedback():
    return render_template('feedback.html', user=current_user)