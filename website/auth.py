from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Data, Feedback
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.orm.exc import NoResultFound

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        try: 
            user = db.session.execute(db.select(User).where(User.email == email)).scalar_one()
        except NoResultFound:  
            user = None

        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.index'))
            else:
                flash('Incorrect wachtwoord', category='error')
        else:
            flash('Email bestaat niet.', category='error') 

    return render_template("login.html", user=current_user)

@auth.route('/logout')
def logout():
    return render_template("login.html")

@auth.route('/sign_up', methods=["GET", "POST"])
def sign_up():
    
    if request.method== 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email is al in gebruik.', category='error')
        elif password1 != password2:
            flash('Wachtwoorden komen niet overeen.', category='error')
        elif len(password1) < 6:
            flash('Wachtwoord is te kort.', category='error')
        else:
            new_user = User(firstname=firstname, lastname=lastname, email=email, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account aangemaakt!', category='success')
            return redirect(url_for('views.index'))
        
    return render_template("sign_up.html")

@auth.route('/feedback', methods=["GET", "POST"])
def feedback():

    if request.method== 'POST':
        feedback = request.form.get('temperatuur')
        new_feedback = Feedback(feedback=feedback)
        db.session.add(new_feedback)
        db.session.commit()
        flash('Feedback succesvol gegeven!', category='success')
        return redirect(url_for('views.index'))
    
    return render_template("feedback.html")
    