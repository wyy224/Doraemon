import logging
import os
from sqlalchemy import true, false

from app.functions import *
from app.models import *
import calendar
from datetime import datetime
from flask import render_template, redirect, flash, url_for, session, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from app import app, db, Config


# from app.forms import LoginForm, SignupForm, YearForm, UpdateForm
# from app.models import User, Notes

# logger = logging.getLogger(__name__)
@app.route('/')
def base():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/icon')
def icon():
    return render_template('icon.html')


@app.route('/product')
def product():
    return render_template('product.html')


@app.route('/service')
def service():
    return render_template('service.html')


@app.route('/typography')
def typography():
    return render_template('typography.html')


@app.route('/shop')
def shop():
    return render_template('shop.html')


@app.route('/single')
def single():
    return render_template('single.html')


# @app.route('/setdatabase')
# def set_database():
#     db.drop_all()
#     db.create_all()
#     return redirect('/base')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form["email"] == "":
            user_find = User.query.filter(User.user_name==request.form["username2"]).first()
            if not user_find:
                flash('No user found with username: {}'.format(request.form["username2"]))
                return redirect(url_for('login'))
            if (check_password_hash(user_find.password_hash, request.form["password"])):
                flash('Login success!')
                session["USERNAME"] = user_find.user_name
                session['Logged_in'] = True
                return redirect(url_for('main_page'))
            else:
                flash('Incorrect Password')
                return redirect(url_for('login'))
        
        else:
            user_in_db = User.query.filter(User.user_name==request.form["username1"]).first()
            if user_in_db:
                flash('User has sign up!')
            else:
                if request.form["password1"] != request.form["password2"]:
                    flash('Passwords do not match!')
                    return redirect(url_for('main_page'))
                else:
                    passw_hash = generate_password_hash(request.form["password1"])
                    user = User(user_name=request.form["username1"], email=request.form["email"], password_hash=passw_hash)
                    db.session.add(user)
                    db.session.commit()
                    flash('User registered with username:{}'.format(request.form["username1"]))
                    session['USERNAME'] = user.user_name
                    session['Logged_in'] = True
                    print(session)
                    return redirect(url_for('main_page'))
    return render_template('login.html')


@app.route('/main_page')
def main_page():
    if islogined():
        name = session['USERNAME']
    else:
        name = "visitor"
    return render_template('index.html', islogin=islogined(), username=name)


@app.route('/commodity', methods=['GET', 'POST'])
def getcommodity():
    data = Commodity.query
    commodity = data.order_by(Commodity.release_time)
    return render_template("index.html", commodity=commodity)

# reset the database
@app.route('/reset_db')
def reset_db():
    set_db()
    return redirect('/')