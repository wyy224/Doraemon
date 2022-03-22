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

all_type = dict({
    '1': 'drum',
    '2': 'piano'
})


# logger = logging.getLogger(__name__)
@app.route('/')
def base():
    return render_template('index.html', islogin=islogined(), types=all_type, type_value=all_type.values())


@app.route('/about')
def about():
    return render_template('about.html', islogin=islogined(), types=all_type, type_value=all_type.values())


@app.route('/contact')
def contact():
    return render_template('contact.html', types=all_type, type_value=all_type.values())


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/icon')
def icon():
    return render_template('icon.html')


@app.route('/product')
def product():
    types = request.args.get('type', None)
    if not types:
        return redirect(url_for('base'))
    if not all_type[types]:
        return redirect(url_for('base'))

    products = Commodity.query.filter_by(type=all_type[types]).all()
    return render_template('product.html', products=products, types=all_type, type_value=all_type.values())


@app.route('/service')
def service():
    return render_template('service.html', islogin=islogined(), types=all_type, type_value=all_type.values())


@app.route('/typography')
def typography():
    return render_template('typography.html')


@app.route('/shop')
def shop():
    commodities = Commodity.query.all()
    new_commodities = Commodity.query.order_by(Commodity.id.desc()).all()[0:5]
    return render_template('shop.html', islogin=islogined(), commodities=commodities, new_commodities=new_commodities,
                           types=all_type, type_value=all_type.values())


@app.route('/single')
def single():
    return render_template('single.html', islogin=islogined())


@app.route('/home')
def home():
    user = User.query.filter(User.user_name == session.get('USERNAME')).first()
    return render_template('home.html', islogin=islogined(), user=user, types=all_type, type_value=all_type.values())


@app.route('/collection')
def collection():
    return render_template('collection.html', islogin=islogined())


# @app.route('/setdatabase')
# def set_database():
#     db.drop_all()
#     db.create_all()
#     return redirect('/base')

# Separate registration from login lnx
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form["email"] == "":
            return login_mes()
        else:
            return reg_mes()
    else:
        return render_template('login.html')
    return render_template('login.html')


@app.route('/login/login_mes')
def login_mes():
    user_find = User.query.filter(User.user_name == request.form["username2"]).first()
    if not user_find:
        flash('Incorrect username')
        return redirect(url_for('login'))
    if (check_password_hash(user_find.password_hash, request.form["password"])):
        flash('Login success!')
        session["USERNAME"] = user_find.user_name
        session['Logged_in'] = True
        return redirect(url_for('main_page'))
    else:
        flash('Incorrect Password')
        return redirect(url_for('login'))


@app.route('/login/reg_mes')
def reg_mes():
    user_in_db = User.query.filter(User.user_name == request.form["username1"]).first()
    if user_in_db:
        flash('User has sign up!')
        return redirect(url_for('login'))
    else:
        if request.form["password1"] != request.form["password2"]:
            flash('Passwords do not match!')
            return redirect(url_for('login'))
        else:
            passw_hash = generate_password_hash(request.form["password1"])
            user = User(user_name=request.form["username1"], email=request.form["email"], password_hash=passw_hash)
            db.session.add(user)
            db.session.commit()
            flash('User registered with username:{}'.format(request.form["username1"]))
            session['USERNAME'] = user.user_name
            print(session)
            return redirect(url_for('main_page'))


@app.route('/api/logout', methods=["GET", "POST"])
def logout():
    session.pop("USERNAME", None)
    return jsonify({'returnValue': 1})


@app.route('/main_page')
def main_page():
    if islogined():
        name = session['USERNAME']
    else:
        name = "visitor"
    return render_template('index.html', islogin=islogined(), username=name)


@app.route('/commodity', methods=['GET', 'POST'])
def get_commodity():
    data = Commodity.query
    commodity = data.order_by(Commodity.release_time)
    return render_template("index.html", commodity=commodity)


# @app.route('/division', methods=['GET', 'POST'])
# def division():
#     return render_template("base.html", types=all_type)


# @app.route('/shop')
# def show_commodity():
#
#     return render_template("shop.html", )


# reset the database
@app.route('/reset_db')
def reset_db():
    set_db()
    return redirect('/')

# @app.route('/add_db')
# def add_db():
#     piano = Commodity(commodity_name='piano', cargo_quantity=100, pic_path='../static/instruments/piano.jpg',
#                       price=3000, introduction='piano', type='piano')
#     db.session.add(piano)
#
#     db.session.commit()
#     return redirect('/')
