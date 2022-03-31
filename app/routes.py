import logging
import os
from sqlalchemy import true, false

from app.functions import *
from app.models import *
from app.forms import UpdateForm
import calendar
from datetime import datetime
from flask import render_template, redirect, flash, url_for, session, request, jsonify, send_from_directory
from werkzeug.security import check_password_hash, generate_password_hash
from flask_avatars import Avatars
from sqlalchemy import and_

from app import app, db, Config

# from app.forms import LoginForm, SignupForm, YearForm, UpdateForm
# from app.models import User, Notes

all_type = dict({
    '1': 'drum',
    '2': 'piano'
})

avatars = Avatars()


# logger = logging.getLogger(__name__)
@app.route('/')
def base():
    user = User.query.filter(User.user_name == session.get('USERNAME')).first()
    user_icon = setIcon()
    return render_template('index.html', islogin=islogined(), user=user, types=all_type, type_value=all_type.values(),
                           icon=user_icon)


@app.route('/about')
def about():
    return render_template('about.html', islogin=islogined(), types=all_type, type_value=all_type.values())


@app.route('/contact')
def contact():
    return render_template('contact.html', types=all_type, type_value=all_type.values())


@app.route('/ShoppingCart')
def ShoppingCart():
    return render_template('ShoppingCart.html', types=all_type, type_value=all_type.values())


@app.route('/api/ShoppingCart/get_pro', methods=['GET'])
def get_cart():
    products = db.session.query(Cart).filter(Cart.user_id == session.get('uid')).all()
    list = []
    for prod in products:
        item = dict()
        pd = Commodity.query.filter(Commodity.id == prod.commodity_id).first()
        item['pic'] = pd.pic_path
        item['name'] = pd.commodity_name
        item['price'] = pd.price
        item['num'] = prod.commodity_num
        list.append(item)
    return jsonify({'products': list})


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/icon')
def icon():
    return render_template('icon.html', types=all_type, ype_value=all_type.values())


@app.route('/product')
def product():
    types = request.args.get('type', None)
    if not types:
        return redirect(url_for('base'))
    if not all_type[types]:
        return redirect(url_for('base'))

    products = Commodity.query.filter_by(type=all_type[types]).all()
    if islogined():
        authority = session['authority']
    else:
        authority = 0
    new_commodities = Commodity.query.order_by(Commodity.id.desc()).all()[0:5]
    return render_template('product.html', products=products, types=all_type, type_value=all_type.values(),
                           authority=authority, new_commodities=new_commodities)


@app.route('/service')
def service():
    return render_template('service.html', islogin=islogined(), types=all_type, type_value=all_type.values())


@app.route('/typography')
def typography():
    return render_template('typography.html', types=all_type, ype_value=all_type.values())


@app.route('/shop', methods=['GET', 'POST'])
def shop():
    commodities = Commodity.query.all()
    new_commodities = Commodity.query.order_by(Commodity.id.desc()).all()[0:5]
    user_id = session.get('uid')
    return render_template('shop.html', islogin=islogined(), commodities=commodities, new_commodities=new_commodities,
                           types=all_type, type_value=all_type.values(), user_id=user_id)


@app.route('/collect', methods=['GET', 'POST'])
def collect():
    user_id = request.form.get("user_id")
    commodity_id = request.form.get("commodity_id")
    exist = Collections.query.filter_by(user_id=user_id, commodity_id=commodity_id).first()
    if exist is not None:
        db.session.delete(exist)
        db.session.commit()
        return "cancel collect"
    else:
        collect1 = Collections(user_id=user_id, commodity_id=commodity_id)
        db.session.add(collect1)
        db.session.commit()
        return "collect success"


@app.route('/adjust_icon', methods=['GET', 'POST'])
def adjust_icon():
    user_id = request.form.get("user_id")
    commodity_id = request.form.get("commodity_id")
    exist = Collections.query.filter_by(user_id=user_id, commodity_id=commodity_id).first()
    if exist is not None:
        return "#ffc107"
    else:
        return "#00b9ff"




@app.route('/single/<int:id>', methods=['GET', 'POST'])
def single(id):
    if islogined():
        authority = session['authority']
    else:
        authority = 0
    commodity = Commodity.query.get(int(id))
    return render_template('single.html', islogin=islogined(), commodity=commodity, types=all_type,
                           type_value=all_type.values(), authority=authority)


# determine if user is logged in or not, if not, jump to login page
@app.route("/cart/add", methods=['GET', 'POST'])
def cart_add():
    if request.method == 'POST':
        if session.get('uid') is not None:
            commodity_id = request.form.get('commodity_id', None)
            commodity_num = request.form.get('num', None)
            user_id = session.get('uid')
            c = Cart.query.filter(and_(Cart.user_id == user_id, Cart.commodity_id == commodity_id)).first()
            # if commodity is already in cart, directly add commodity_num
            if c is not None:
                c.commodity_num = str(int(c.commodity_num) + int(commodity_num))
            else:
                cart = Cart(commodity_id=commodity_id, commodity_num=commodity_num, user_id=user_id)
                db.session.add(cart)
            db.session.commit()
            return redirect(url_for('ShoppingCart'))
        else:
            return redirect(url_for('login'))


@app.route('/newsingle', methods=['GET', 'POST'])
def newsingle():
    if request.method == 'POST':
        print("1111111")
        newcommodity = Commodity(commodity_name=request.form['product name'], cargo_quantity=request.form['quantity'],
                                 # pic_path='../static/instruments/piano.jpg',
                                 price=request.form['price'], introduction=request.form['introduction'],
                                 type=request.form['type'])
        db.session.add(newcommodity)
        db.session.commit()
        session['cid'] = newcommodity.id
        print("22222222")
        return redirect(url_for('product'))
    else:
        return render_template('newsingle.html', islogin=islogined())


@app.route('/home')
def home():
    if islogined():
        user = User.query.filter(User.user_name == session.get('USERNAME')).first()
        profile = Profile.query.filter(Profile.user_id == user.id).first()
        user_icon = setIcon()
        print(user_icon)
        if profile.address == None:
            profile.address = ''
        if profile.phone_num == None:
            profile.phone_num = ''
        if profile.name == None:
            profile.name = ''
        return render_template('home.html', islogin=islogined(), user=user, profile=profile, types=all_type,
                               type_value=all_type.values(), icon=user_icon)
    else:
        return redirect(url_for('login'))


@app.route('/collection')
def collection():
    user = User.query.filter(User.user_name == session.get('USERNAME')).first()
    user_icon = setIcon()
    collects = Collections.query.filter(Collections.user_id == session.get('uid'))
    return render_template('collection.html', user=user, icon=user_icon, islogin=islogined(), collects=collects)


@app.route('/modify', methods=['GET', 'POST'])
def modify():
    user = User.query.filter(User.user_name == session.get('USERNAME')).first()
    user_icon = setIcon()
    profile = Profile.query.filter(Profile.user_id == user.id).first()
    form = UpdateForm()
    ava_dir = Config.AVA_UPLOAD_DIR
    # change profile
    if form.validate_on_submit():
        user.user_name = form.username.data
        user.email = form.email.data
        profile.address = form.address.data
        profile.phone_num = form.phone_num.data
        profile.name = form.name.data

        # change avatar
        if form.avatar.data:
            file_obj = form.avatar.data
            ava_filename = session.get("USERNAME") + '_AVA.jpeg'
            file_obj.save(os.path.join(ava_dir, ava_filename))
            flash('AVA uploaded and saved')
            user.icon = ava_filename.encode()
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('modify.html', islogin=islogined(), user=user, icon=user_icon, profile=profile, form=form)


# To get the avatar
def setIcon():
    if islogined():
        user = User.query.filter(User.user_name == session.get('USERNAME')).first()
        user_icon = user.icon
        if user_icon != None:
            icon = user.icon
            user_icon = url_for('static', filename='uploaded_AVA/' + icon)
        else:
            user_icon = 'NULL'
    else:
        user_icon = 'NULL'
    return user_icon


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
        session['uid'] = user_find.id
        session['authority'] = user_find.authority
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
            session['uid'] = user.id
            print(session)
            return redirect(url_for('main_page'))


# bug
@app.route('/api/logout', methods=["GET", "POST"])
def logout():
    # session.pop("USERNAME", None)
    # session.pop("uid", None)
    # return jsonify({'returnValue': 1})
    session.clear()
    return redirect('/main_page')


@app.route('/main_page')
def main_page():
    if islogined():
        name = session['USERNAME']
        user_icon = setIcon()
    else:
        name = "visitor"
    return render_template('index.html', islogin=islogined(), username=name, types=all_type,
                           ype_value=all_type.values(), icon=user_icon)


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


# Icon
@app.route('/img/<path:filename>')
def get_avatar(filename):
    return send_from_directory((os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploaded_AVA')),
                               filename, as_attachment=True)


@app.route('/change-avatar/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        raw_filename = avatars.save_avatar(f)
        session['raw_filename'] = raw_filename
        print("app/static/uploaded_AVA/" + session['raw_filename'])
        print(os.path.join(os.path.abspath(os.path.dirname(__file__))))
        u = session['uid']
        avatar = User.query.filter(User.id == u).first()
        # avatar.icon = "app/static/uploaded_AVA/" + session['raw_filename']
        avatar.icon = session['raw_filename']
        db.session.commit()
        return redirect("/change-avatar/crop/")
    return render_template('upload.html')


@app.route('/change-avatar/crop/', methods=['GET', 'POST'])
def crop():
    if request.method == 'POST':
        x = request.form.get('x')
        y = request.form.get('y')
        w = request.form.get('w')
        h = request.form.get('h')
        user = User.query.filter(User.user_name == session["USERNAME"]).first()
        filenames = avatars.crop_avatar(session['raw_filename'], x, y, w, h)
        url_s = filenames[0]
        url_m = filenames[1]
        url_l = filenames[2]
        # user.icon = "app/static/uploaded_AVA/" + url_l
        user.icon = url_l
        db.session.commit()
        flash('Change avatar successfully', 'success')

        return redirect("/home")
    return render_template('crop.html')

# add commodity
@app.route('/img/<path:filename>', endpoint="commodity_pic")
def get_commodity(filename):
    return send_from_directory((os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/commodity')),
                               filename, as_attachment=True)

@app.route('/change-commodity/', methods=['GET', 'POST'])
def upload_commodity():
    if request.method == 'POST':
        f = request.files.get('file')
        raw_filename = avatars.save_avatar(f)
        session['raw_filename'] = raw_filename
        print("app/static/commodity/" + session['raw_filename'])
        c = session['cid']
        commodity = Commodity.query.filter(Commodity.id == c).first()
        commodity.pic_path = session['raw_filename']
        db.session.commit()
        return redirect("/change-commodity/crop/")
    return render_template('upload.html')


@app.route('/change-commodity/crop/', methods=['GET', 'POST'])
def commodity_crop():
    if request.method == 'POST':
        x = request.form.get('x')
        y = request.form.get('y')
        w = request.form.get('w')
        h = request.form.get('h')
        commodity = Commodity.query.filter(Commodity.id == session["cid"]).first()
        filenames = avatars.crop_avatar(session['raw_filename'], x, y, w, h)
        url_s = filenames[0]
        url_m = filenames[1]
        url_l = filenames[2]
        commodity.pic_path = url_l
        db.session.commit()

        return redirect("/shop")
    return render_template('crop.html')
