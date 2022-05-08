import logging
import os
import json
from uuid import uuid4

from flask_socketio import SocketIO, join_room, leave_room
from PIL import Image
from sqlalchemy import true, false

from app.functions import *
from app.models import *
from app.forms import UpdateForm, ReviewForm
import calendar
from datetime import datetime, timedelta
from flask import render_template, redirect, flash, url_for, session, request, jsonify, send_from_directory, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from flask_avatars import Avatars
from sqlalchemy import and_, distinct

from app import app, db, Config

# from app.forms import LoginForm, SignupForm, YearForm, UpdateForm
# from app.models import User, Notes

all_type = dict({
    '1': 'drum',
    '2': 'piano',
    '3': 'horn',
    '4': 'trombone',
    '5': 'trumpet',
    '6': 'violin',
})

avatars = Avatars()

socketio = SocketIO()
socketio.init_app(app)


# logger = logging.getLogger(__name__)
@app.route('/')
def base():
    user = User.query.filter(User.user_name == session.get('USERNAME')).first()
    if islogined():
        user_icon = setIcon()
        authority = session.get('authority')
    else:
        user_icon = 'NULL'
        authority = 0
    return render_template('index.html', islogin=islogined(), user=user, types=all_type, type_value=all_type.values(),
                           icon=user_icon, authority=authority)


@app.route('/search', methods=['GET', 'POST'])
def search():
    search_result = request.form.get("search_result")

    if search_result == '' or search_result is None:
        return redirect(url_for('base'))

    final_search = Commodity.query.filter(Commodity.commodity_name.like("%" + search_result + "%")).all()

    return render_template('SearchResults.html', final_search=final_search, types=all_type,
                           type_value=all_type.values())


# @app.route('/customer_search', methods=['GET', 'POST'])
# def find_customer():
#     print("11111111111111111111111111111")
#     uid = request.args.get("uid")
#     uname = request.args.get("uname")
#     email = request.args.get("email")
#     filterList = []
#     if uid is not None:
#         filterList.append(User.id.like('%'+uid+'%'))
#     if uname is not None:
#         filterList.append(User.id.like('%'+uname+'%'))
#     if email is not None:
#         filterList.append(User.id.like('%'+email+'%'))
#
#     user = User.query.filter(*filterList).all()
#
#     return render_template('customer.html', user=user)


@app.route('/about')
def about():
    if islogined():
        user_icon = setIcon()
        authority = session.get('authority')
    else:
        user_icon = 'NULL'
        authority = 0
    return render_template('about.html', islogin=islogined(), icon=user_icon, types=all_type,
                           type_value=all_type.values(), authority=authority)


room_user = {}


@app.route('/contact')
def contact():
    if islogined():
        user = User.query.filter(User.id == session.get('uid')).first()
        if (user.ban == 1):
            flash('The user has been disabled')
            return redirect(url_for('log_out'))
        user_icon = setIcon()
        authority = session.get('authority')
        username = session.get('USERNAME')
        user = User.query.filter(User.authority == 0).all()
        uid = session.get('uid')
        if session.get('authority') == 0:
            room = session.get('uid')
            room_num = str(room)
            session['room'] = room
            message = Message.query.filter_by(room=room_num).all()
        else:
            return redirect(url_for('adjust'))

    else:
        user_icon = 'NULL'
        return redirect(url_for('login'))

    return render_template('contact.html', islogin=islogined(), icon=user_icon, types=all_type,
                           type_value=all_type.values(), authority=authority, username=username, user=user, room=room,
                           message=message, uid=uid)


@app.route('/contact_admin/<int:id>', methods=['GET', 'POST'])
def contact_admin(id):
    if islogined():
        user_icon = setIcon()
        authority = session.get('authority')
        username = session.get('USERNAME')
        user = User.query.filter(User.authority == 0).all()
        uid = session.get('uid')
        room = id
        room_num = str(id)
        session['room'] = room
        message = Message.query.filter_by(room=room_num).all()
        choose1 = User.query.filter(User.id == id).first()
        choose1.situation = True
        db.session.commit()
        contact_user = User.query.filter(User.id == id).first()
        contact_icon = contact_user.icon


    else:
        user_icon = 'NULL'
        return redirect(url_for('login'))
    return render_template('contact.html', islogin=islogined(), icon=user_icon, types=all_type,
                           type_value=all_type.values(), authority=authority, username=username, user=user, room=room,
                           message=message, uid=uid, contact_icon=contact_icon)


@app.route('/adjust', methods=['GET', 'POST'])
def adjust():
    user = User.query.filter_by(authority=0).order_by((User.situation == 0).desc()).all()

    if request.method == 'POST':
        uid = request.form.get("uid")
        uname = request.form.get("uname")
        filterList = []
        if uid != '':
            filterList.append(User.id == uid)

        if uname != '':
            filterList.append(User.user_name.like('%' + uname + '%'))

        filterList.append(User.authority==0)


        user = User.query.filter(*filterList).all()


    return render_template('adjust.html', user=user)


# # 连接
@socketio.on('connect')
def handle_connect():
    username = session.get('USERNAME')
    # online_user.append(username)
    # print('connect info:  ' + f'{username}  connect')
    # print(online_user)
    # socketio.emit('connect info', f'{username}  connect')


# 断开连接
# @socketio.on('disconnect')
# def handle_disconnect():
#     username = session.get('USERNAME')
#     print('connect info:  ' + f'{username}  disconnect')
#     # socketio.emit('connect info', f'{username}  disconnect')


# @socketio.on('connect info')
# def handle_connect_info(info):
#     print('connect info' + str(info))
#     room = session.get('room')
#     socketio.emit('connect info', info, to=room)


@socketio.on('send msg')
def handle_message(data):
    print('sendMsg' + str(data))
    room = str(session['room'])
    print(room)
    message = Message(author_id=session['uid'], room=room, content=data.get('message'), user_name=data.get('user'))
    db.session.add(message)
    user = User.query.filter_by(id=room).first()
    user.new_time = datetime.now()
    user.count = user.count + 1
    user.situation = False
    db.session.commit()
    data['message'] = data.get('message').replace('<', '&lt;').replace('>', '&gt;').replace(' ', '&nbsp;')

    socketio.emit('send msg', data, to=room)


@socketio.on('join')
def on_join(data):
    username = data.get('username')
    room = data.get('room')
    try:
        room_user[room].append(username)
    except:
        room_user[room] = []
        room_user[room].append(username)

    join_room(room)
    print('join room:  ' + str(data))
    print(room_user)
    socketio.emit('connect info', username + ' join room', to=room)


@socketio.on('leave')
def on_leave(data):
    username = data.get('username')
    room = data.get('room')
    room_user[room].remove(username)
    leave_room(room)
    print('leave room   ' + str(data))
    print(room_user)
    socketio.emit('connect info', username + ' leave room', to=room)


@app.route('/ShoppingCart')
def ShoppingCart():
    if islogined():
        user = User.query.filter(User.id == session.get('uid')).first()
        if (user.ban == 1):
            flash('The user has been disabled')
            return redirect(url_for('log_out'))
        else:
            return render_template('ShoppingCart.html', types=all_type, type_value=all_type.values())
    else:
        return redirect(url_for('login'))


@app.route('/SearchResults')
def SearchResults():
    return render_template('SearchResults.html', types=all_type, type_value=all_type.values())


@app.route('/api/ShoppingCart/get_pro', methods=['GET'])
def get_cart():
    products = db.session.query(Cart).filter(Cart.user_id == session.get('uid')).all()
    list = []
    for prod in products:
        item = dict()
        pd = Commodity.query.filter(Commodity.id == prod.commodity_id).first()
        item['pic'] = pd.pic_path1
        item['name'] = pd.commodity_name
        item['price'] = pd.price
        item['num'] = prod.commodity_num
        list.append(item)
    return jsonify({'products': list})


@app.route('/api/ShoppingCart/change', methods=['POST'])
def change_cart():
    commodity_name = request.form.get('name')
    num = request.form['num']
    type = request.form['type']
    print(type)
    if type == 'delAll':
        products = db.session.query(Cart).filter(Cart.user_id == session.get('uid')).all()
        for prod in products:
            db.session.delete(prod)
        db.session.commit()
        return jsonify({'returnValue': 1})
    pd = Commodity.query.filter(Commodity.commodity_name == commodity_name).first()
    product = db.session.query(Cart).filter(Cart.user_id == session.get('uid'), Cart.commodity_id == pd.id).first()
    if type == 'add':
        product.commodity_num = product.commodity_num + 1
    elif type == 'reduce':
        product.commodity_num = product.commodity_num - 1
    elif type == 'change':
        product.commodity_num = num
    elif type == 'delete':
        db.session.delete(product)
    db.session.commit()
    return jsonify({'returnValue': 1})


# @app.route('/ShoppingCart/purchase', methods=['GET', 'POST'])
# def pay_from_cart():
#     data = request.get_data()
#     print(data)
#     json_data = json.loads(data.decode("utf-8"))
#     c_name = json_data.get("name")
#     commodity = Commodity.query.filter(Commodity.commodity_name == c_name).first()
#     session['cid'] = commodity.id
#     print(json_data.get("num"))
#     session['cart_num'] = json_data.get("num")
#     return redirect('/ShoppingCart/purchase/going')
#
#
# @app.route('/ShoppingCart/purchase/going')
# def going():
#     return redirect('/purchase')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/icon')
def icon():
    return render_template('icon.html', types=all_type, type_value=all_type.values())


@app.route('/product')
def product():
    types = request.args.get('type', None)
    if not types:
        return redirect(url_for('base'))
    if not all_type[types]:
        return redirect(url_for('base'))
    page = request.args.get('page', 1, type=int)
    products = Commodity.query.filter_by(type=all_type[types]).paginate(page,
                                                                        per_page=5,
                                                                        error_out=False)
    user_id = session.get('uid')
    for commodity in products.items:
        collections = Collections.query.filter_by(user_id=user_id, commodity_id=commodity.id).first()
        if collections:
            commodity.is_collected = True
        else:
            commodity.is_collected = False

    if islogined():
        authority = session.get('authority')
        user_icon = setIcon()
    else:
        authority = 0
        user_icon = 'NULL'
    new_commodities = Commodity.query.order_by(Commodity.id.desc()).all()[0:5]
    x = new_commodities
    for a in x:
        a.release_time = a.release_time.strftime('%Y-%m-%d')
    return render_template('product.html', islogin=islogined(), products=products, types=all_type,
                           type_value=all_type.values(),
                           authority=authority, new_commodities=x, icon=user_icon, type=types,
                           user_id=user_id)


@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    if islogined():
        user = User.query.filter(User.id == session.get('uid')).first()
        print(user)
        if (user.ban == 1):
            flash('The user has been disabled')
            return redirect(url_for('log_out'))
        print(session.get('cid'))
        commodity = Commodity.query.filter(Commodity.id == session.get('cid')).first()
        cart_pay = None
        showList = []
        info = dict()
        print(session.get('order_list'))
        num = 0
        if session.get('order_list') is not None:
            price = session.get('price')
            cart_pay = session.get('order_list')
            for c in session.get('order_list'):
                info = dict()
                c_name = c['name']
                commodity = Commodity.query.filter(Commodity.commodity_name == c_name).first()
                info['commodity'] = commodity
                info['num'] = c['num']
                showList.append(info)
                print(info)
                print(showList)
        else:
            price = commodity.price
            num = session['purchase_num']
        profile = Profile.query.filter(Profile.user_id == session.get('uid')).first()
        if request.method == 'POST':
            # user = User.query.filter(User.user_name == session.get('USERNAME')).first()
            # quantity = int(request.form['quantity'])
            # priceNeed = int(commodity.price)
            # if user.money >= priceNeed * quantity:
            # neworder = Order(commodity_id=session['cid'], user_id=session['uid'],
            #                  commodity_num=quantity, address=request.form['address'],
            #                  transport=request.form['transport'])
            neworder = Order(user_id=session.get('uid'), address=request.form['address'],
                             transport=request.form['transport'], phone_num=request.form['phone_num'],
                             name=request.form['name'])
            # user.money = user.money - priceNeed * quantity
            db.session.add(neworder)
            # db.session.commit()
            user = User.query.filter(User.user_name == session.get('USERNAME')).first()
            if session.get('order_list') is not None:
                if user.money >= int(session.get('price')):
                    user.money = user.money - int(session.get('price'))
                    for c in session.get('order_list'):
                        c_name = c['name']
                        c_num = c['num']
                        com = Commodity.query.filter(Commodity.commodity_name == c_name).first()
                        orderdetail = OrderDetail(commodity_id=com.id, order_id=neworder.id, commodity_num=c_num)
                        db.session.add(orderdetail)
                        if (com.cargo_quantity < int(c_num)):
                            message = "No more stock"
                            return render_template('payfail.html', message=message)

                        com.cargo_quantity -= int(c_num)
                        cart = Cart.query.filter(Cart.commodity_id == com.id).all()
                        for a in cart:
                            db.session.delete(a)
                else:
                    message = "Insufficient account balance"
                    return (render_template('payfail.html', message=message))
            else:

                quantity = int(request.form['num'])
                priceNeed = int(commodity.price)
                if user.money >= priceNeed * quantity:
                    user.money = user.money - priceNeed * quantity
                    com = Commodity.query.filter(Commodity.id == session.get('cid')).first()
                    orderdetail = OrderDetail(commodity_id=session.get('cid'), order_id=neworder.id,
                                              commodity_num=request.form['num'])
                    print("before:", com.cargo_quantity)
                    if com.cargo_quantity < int(request.form['num']):
                        message = "No more stock"
                        return render_template('payfail.html', message=message)
                    com.cargo_quantity -= int(request.form['num'])
                    print("after:", com.cargo_quantity)
                    db.session.add(orderdetail)
                else:
                    message = "Insufficient account balance"
                    return (render_template('payfail.html', message=message))
            session.pop('cid', None)
            session.pop('order_list', None)
            session.pop('price', None)
            db.session.commit()
            return redirect(url_for('Orders'))

        return render_template('pay.html', commodity=commodity, profile=profile, price=price, cart_pay=cart_pay,
                               showlist=showList, num=num)
    else:
        return redirect('/login')


@app.route('/api/ShoppingCart/purchase', methods=['POST'])
def pay_order():
    name = json.loads(request.form.get('name'))
    num = json.loads(request.form.get('num'))
    commodity_list = []
    i = 0
    for n in name:
        item = dict()
        item['name'] = n
        item['num'] = num[i]
        i = i + 1
        commodity_list.append(item)
    print(commodity_list)
    price = request.form.get('price')
    session['order_list'] = commodity_list
    session.pop('price', None)
    session['price'] = price
    return jsonify({'returnValue': 1})


@app.route('/top_up', methods=['GET', 'POST'])
def topup():
    if islogined():
        user = User.query.filter(User.id == session.get('uid')).first()
        if (user.ban == 1):
            flash('The user has been disabled')
            return redirect(url_for('log_out'))
        username = session['USERNAME']
        if request.method == 'POST':
            requirement = CheckMoney(user_name=session.get('USERNAME'), money=int(request.form['money']))
            # user.money = user.money + int(request.form['money'])
            db.session.add(requirement)
            db.session.commit()
            return redirect(url_for('home'))
        else:
            return render_template('topup.html', username=username)
    else:
        return redirect('/login')


@app.route('/service')
def service():
    if islogined():
        user_icon = setIcon()
        authority = session.get('authority')
        session['cid'] = id
    else:
        user_icon = 'NULL'
        authority = 0
    return render_template('service.html', islogin=islogined(), icon=user_icon, types=all_type,
                           type_value=all_type.values(), authority=authority)


@app.route('/typography')
def typography():
    return render_template('typography.html', types=all_type, ype_value=all_type.values())


@app.route('/shop', methods=['GET', 'POST'])
def shop():
    if islogined():
        authority = session.get('authority')
        user_icon = setIcon()
        # authority = session['authority']
    else:
        authority = 0
        user_icon = 'NULL'
    print(session.get('price_section_start'))
    if session.get('price_section_start') is None:
        commodities = Commodity.query.all()
    else:
        commodities = Commodity.query.filter(
            Commodity.price.between(session.get('price_section_start'), session.get('price_section_end')))
    session.pop('price_section_start', None)
    session.pop('price_section_end', None)
    new_commodities = Commodity.query.order_by(Commodity.id.desc()).all()[0:5]
    collect_commodities = Commodity.query.order_by(Commodity.collect_num.desc()).all()[0:5]
    x = new_commodities

    user_id = session.get('uid')
    user = User.query.filter(User.id == user_id).first()

    for commodity in commodities:
        collections = Collections.query.filter_by(user_id=user_id, commodity_id=commodity.id).first()
        if collections:
            commodity.is_collected = True
        else:
            commodity.is_collected = False

    list = dict()

    for a in x:
        list[a.id] = a.release_time.strftime('%Y-%m-%d')

    return render_template('shop.html', islogin=islogined(), commodities=commodities, new_commodities=x,
                           types=all_type, type_value=all_type.values(), icon=user_icon, user_id=user_id,
                           authority=authority, collect_commodities=collect_commodities, list=list, user=user)


@app.route('/api/shop/price_section', methods=['POST'])
def get_price_section():
    p = int(request.form.get('price'))
    # session.pop('price_section_start',None)
    # session.pop('price_section_end', None)
    if p == 1:
        session['price_section_start'] = 0
        session['price_section_end'] = 1000
    elif 2 <= p < 7:
        session['price_section_start'] = 1000 + (p - 2) * 1500
        session['price_section_end'] = 1000 + (p - 1) * 1500
    elif p >= 7:
        session['price_section_start'] = 7000
        session['price_section_end'] = 100000000
    return jsonify({'returnValue': 1})


@app.route('/collect', methods=['GET', 'POST'])
def collect():
    user_id = request.form.get("user_id")
    commodity_id = request.form.get("commodity")
    exist = Collections.query.filter_by(user_id=user_id, commodity_id=commodity_id).first()
    commodity5 = Commodity.query.filter_by(id=commodity_id).first()
    if exist is not None:
        commodity5.collect_num = commodity5.collect_num - 1
        db.session.delete(exist)
        db.session.commit()
        return "cancel collect"
    else:
        commodity5.collect_num = commodity5.collect_num + 1
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
    session.pop('order_list', None)
    session.pop('price', None)
    if islogined():
        user_icon = setIcon()
    else:
        user_icon = 'NULL'
    if islogined():
        authority = session.get('authority')
        session['cid'] = id
    else:
        authority = 0
    commodity = Commodity.query.get(int(id))
    form = ReviewForm()
    reviews = get_reviews(commodity.id)
    if form.validate_on_submit():
        if session.get('uid') is not None:
            user = User.query.filter(User.id == session.get('uid')).first()
            if (user.ban == 1):
                flash('The user has been disabled')
                return redirect(url_for('log_out'))
            review = Review(user_id=session.get('uid'), commodity_id=commodity.id, title=form.title.data,
                            text=form.text.data)
            db.session.add(review)
            db.session.commit()
            return redirect(url_for('single', id=id))
        else:
            return redirect(url_for('login'))
    return render_template('single.html', islogin=islogined(), icon=user_icon, form=form, reviews=reviews,
                           commodity=commodity,
                           types=all_type,
                           type_value=all_type.values(), authority=authority)

@app.route('/api/music', methods=["GET", "POST"])
def check_music():
    m = request.form.get('music')
    m_name = os.path.basename(m)
    dir = os.path.join(Config.MUSIC_SAVE_PATH, m_name)
    if os.path.exists(dir):
        return jsonify({'returnValue': 1})
    else:
        return jsonify({'returnValue': 0})


def get_reviews(p):
    reviews = db.session.query(Review).filter(Review.commodity_id == p).order_by(Review.created.desc()).all()
    list = []
    for review in reviews:
        item = dict()
        user = db.session.query(User).filter(User.id == review.user_id).first()
        item['ava'] = url_for('static', filename='uploaded_AVA/' + user.icon)
        item['user'] = user.user_name
        item['title'] = review.title
        item['text'] = review.text
        list.append(item)

    return list


# determine if user is logged in or not, if not, jump to login page
@app.route("/cart/add", methods=['GET', 'POST'])
def cart_add():
    if request.method == 'POST':
        if session.get('uid') is not None:
            user = User.query.filter(User.id == session.get('uid')).first()
            if (user.ban == 1):
                flash('The user has been disabled')
                return redirect(url_for('log_out'))
            commodity_id = request.form.get('commodity_id', None)
            commodity_num = request.form['number']
            print(commodity_num)
            user_id = session.get('uid')
            c = Cart.query.filter(and_(Cart.user_id == user_id, Cart.commodity_id == commodity_id)).first()
            # if commodity is already in cart, directly add commodity_num
            if c is not None:
                c.commodity_num = c.commodity_num + int(commodity_num)

            else:
                cart = Cart(commodity_id=commodity_id, commodity_num=commodity_num, user_id=user_id)
                db.session.add(cart)
            db.session.commit()
            return redirect(url_for('ShoppingCart'))
        else:
            return redirect(url_for('login'))


@app.route("/single/add", methods=['GET', 'POST'])
def single_add():
    user = User.query.filter(User.id == session.get('uid')).first()
    if (user.ban == 1):
        flash('The user has been disabled')
        return redirect(url_for('log_out'))
    session['purchase_num'] = request.form['number']
    return redirect(url_for('purchase'))


@app.route('/newProduct', methods=['GET', 'POST'])
def newproduct():
    user = User.query.filter(User.user_name == session.get('USERNAME')).first()
    user_icon = setIcon()
    authority = session.get('authority')
    if request.method == 'POST':
        newcommodity = Commodity(commodity_name=request.form.get('product name'),
                                 cargo_quantity=request.form.get('quantity'),
                                 price=request.form.get('price'), introduction=request.form.get('introduction'),
                                 type=request.form.get('type'))
        dir = "../static/instruments/"
        if request.files.get('pic1').filename != "":
            f = request.files.get('pic1')
            newcommodity.pic_path1 = dir + f.filename
            f.save(os.path.join(Config.AVATARS_SAVE_PATH, f.filename))
        if request.files.get('pic2').filename != "":
            f = request.files.get('pic2')
            newcommodity.pic_path2 = dir + f.filename
            f.save(os.path.join(Config.AVATARS_SAVE_PATH, f.filename))
        if request.files.get('pic3').filename != "":
            f = request.files.get('pic3')
            newcommodity.pic_path3 = dir + f.filename
            f.save(os.path.join(Config.AVATARS_SAVE_PATH, f.filename))
        if request.files.get('sound').filename != "":
            s = request.files.get('sound')
            s_name = newcommodity.commodity_name + ".mp3"
            if os.path.exists(os.path.join(Config.MUSIC_SAVE_PATH, s_name)):
                os.remove(os.path.join(Config.MUSIC_SAVE_PATH, s_name))
            s.save(os.path.join(Config.MUSIC_SAVE_PATH, s_name))
        db.session.add(newcommodity)
        db.session.commit()
        session['cid'] = newcommodity.id
        return redirect(url_for('home'))
    else:
        return render_template('newProduct.html', islogin=islogined(), user=user, icon=user_icon, c=None,
                               authority=authority, types=all_type, type_value=all_type.values())


@app.route('/Orders')
def Orders():
    if islogined():
        user = User.query.filter(User.user_name == session.get('USERNAME')).first()
        if (user.ban == 1):
            flash('The user has been disabled')
            return redirect(url_for('log_out'))
        user_icon = setIcon()
        orders = Order.query.filter(Order.user_id == session.get('uid')).order_by(Order.Urgent.desc()).all()
        allorders = Order.query.order_by(Order.Urgent.desc()).all()
        list = [];
        alllist = []
        for o in orders:
            list = get_orders(o, list)
        session.pop('orders', None)
        session['orders'] = list
        for o2 in allorders:
            alllist = get_orders(o2, alllist)
        session.pop('allorders', None)
        session['allorders'] = alllist
        print(session['allorders'])
        authority = session.get('authority')

        return render_template('order.html', user=user, icon=user_icon, islogin=islogined(), orders=list,
                               allorders=alllist,
                               authority=authority)

    else:
        return redirect(url_for('login'))


@app.route('/singleOrder/<int:id>', methods=['GET', 'POST'])
def singleOrder(id):
    user = User.query.filter(User.user_name == session.get('USERNAME')).first()
    if (user.ban == 1):
        flash('The user has been disabled')
        return redirect(url_for('log_out'))

    user_icon = setIcon()

    allorders = Order.query.all()
    alllist = []
    for o2 in allorders:
        alllist = get_orders(o2, alllist)
    session.pop('allorders', None)
    session['allorders'] = alllist

    list = session.get('allorders')
    print(list)
    order_num = db.session.query(OrderDetail).filter(OrderDetail.id < id).count()
    print(order_num)
    order = list[order_num]

    user1 = User.query.filter(User.id == session.get('uid')).first()
    sta = order['status']

    detail = OrderDetail.query.filter(OrderDetail.id == id).first()

    return render_template('singleOrder.html', user=user, icon=user_icon, islogin=islogined(), order=order, user1=user1,
                           sta=sta, detail=detail)


@app.route('/status/<int:id>', methods=['GET', 'POST'])
def change_status(id):
    status = request.form['status']
    list = session.get('allorders')
    order1 = list[int(id) - 1]
    order = Order.query.filter(Order.id == order1['id']).first()
    order.status = status
    db.session.commit()
    return redirect(url_for('singleOrder', id=id))


def get_orders(p, list):
    order_detail = db.session.query(OrderDetail).filter(OrderDetail.order_id == p.id).all()
    order_detail1 = db.session.query(Order).filter(Order.id == p.id).first()

    for od in order_detail:
        item = dict()
        c = db.session.query(Commodity).filter(Commodity.id == od.commodity_id).first()
        item['id'] = p.id
        item['detail'] = od.id
        item['pic_path'] = c.pic_path1
        item['status'] = p.status
        item['commodity_name'] = c.commodity_name
        item['purchase_time'] = p.purchase_time
        item['address'] = p.address
        item['introduction'] = c.introduction
        item['price'] = c.price * od.commodity_num
        item['transport'] = p.transport
        item['name'] = order_detail1.name
        item['phone_num'] = order_detail1.phone_num
        item['urgent'] = p.Urgent
        list.append(item)

    return list


@app.route('/singleOrder/order/delete/<int:id>', methods=['GET', 'POST'])
def deleteOrder(id):
    user = User.query.filter(User.id == session.get('uid')).first()
    if (user.ban == 1):
        flash('The user has been disabled')
        return redirect(url_for('log_out'))
    od_del = OrderDetail.query.get(id)
    # check if one order has multiple details
    details = db.session.query(OrderDetail).filter(OrderDetail.order_id == od_del.order_id).all()
    # if has only one detail then delete the order
    money = 0
    for a in details:
        db.session.delete(a)
        commodity = Commodity.query.filter(Commodity.id == a.commodity_id).first()
        money = money + commodity.price * a.commodity_num
        commodity.cargo_quantity = commodity.cargo_quantity + a.commodity_num
    order = Order.query.filter(Order.id == od_del.order_id).first()
    user = User.query.filter(User.id == order.user_id).first()
    user.money = user.money + money
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for('Orders'))


@app.route('/singleOrder/order/urgent/<int:id>', methods=['GET', 'POST'])
def urgent(id):
    od_del = OrderDetail.query.get(id)
    details = db.session.query(OrderDetail).filter(OrderDetail.order_id == od_del.order_id).first()
    order = Order.query.filter(Order.id == details.order_id).first()
    if (order.Urgent):
        order.Urgent = 0
    else:
        order.Urgent = 1
    db.session.commit()
    return redirect(url_for('singleOrder', id=id))


@app.route('/singleOrder/order/receive/<int:id>', methods=['GET', 'POST'])
def receiveOder(id):
    user = User.query.filter(User.id == session.get('uid')).first()
    if (user.ban == 1):
        flash('The user has been disabled')
        return redirect(url_for('log_out'))
    list = session.get('allorders')
    order1 = list[int(id) - 1]
    order = Order.query.filter(Order.id == order1['id']).first()
    order.status = "Signed in"
    order.Urgent = 0
    db.session.commit()
    return redirect(url_for('singleOrder', id=id))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    user = User.query.filter(User.id == session.get('uid')).first()
    if (user.ban == 1):
        flash('The user has been disabled')
        return redirect(url_for('log_out'))
    od_ed = OrderDetail.query.get(id)
    details = db.session.query(Order).filter(Order.id == od_ed.order_id).first()

    if request.method == 'POST':
        details.address = request.form['address']
        details.phone_num = request.form['phone_num']
        details.name = request.form['name']
        details.transport = request.form['transport']
        db.session.commit()
        return redirect(url_for('singleOrder', id=id))

    return render_template('editorder.html', details=details)


@app.route('/home')
def home():
    if islogined():
        user = User.query.filter(User.user_name == session.get('USERNAME')).first()
        if (user.ban == 1):
            flash('The user has been disabled')
            return redirect(url_for('log_out'))
        else:
            profile = Profile.query.filter(Profile.user_id == user.id).first()
            user_icon = setIcon()
            authority = session.get('authority')
            if profile.address == None:
                profile.address = ''
            if profile.phone_num == None:
                profile.phone_num = ''
            if profile.name == None:
                profile.name = ''
            info = get_info()
            new = get_new()
            return render_template('home.html', islogin=islogined(), user=user, profile=profile, types=all_type,
                                   type_value=all_type.values(), info=info, new=new, icon=user_icon,
                                   authority=authority)
    else:
        return redirect(url_for('login'))


def get_info():
    info = dict()
    prod = Commodity.query.count()
    user = int(User.query.count()) - 1
    order = Order.query.count()
    info['prod'] = prod
    info['cus'] = user
    info['order'] = order
    return info


def get_new():
    NOW = datetime.now()
    new = dict()
    order = Commodity.query.filter(Order.purchase_time >= NOW - timedelta(days=1)).count()
    cus = User.query.filter(User.register_time >= NOW - timedelta(days=1)).count()
    cmnt = Review.query.filter(Review.created >= NOW - timedelta(days=1)).count()
    new['order'] = order
    new['cus'] = cus
    new['cmnt'] = cmnt
    return new


@app.route('/collection')
def collection():
    if islogined():
        user = User.query.filter(User.user_name == session.get('USERNAME')).first()
        if (user.ban == 1):
            flash('The user has been disabled')
            return redirect(url_for('log_out'))
        else:
            user_icon = setIcon()
            authority = session.get('authority')
            collects = Collections.query.filter(Collections.user_id == session.get('uid'))
            return render_template('collection.html', user=user, icon=user_icon, islogin=islogined(), collects=collects,
                                   authority=authority)
    else:
        return redirect(url_for('login'))


@app.route('/CheckTopup')
def CheckTopup():
    user = User.query.filter(User.user_name == session.get('USERNAME')).first()
    if (user.ban == 1):
        flash('The user has been disabled')
        return redirect(url_for('log_out'))
    user_icon = setIcon()
    authority = session.get('authority')
    if (authority == 0):
        check = CheckMoney.query.filter(CheckMoney.user_name == session.get('USERNAME')).all()
    else:
        check = CheckMoney.query.all()
    return render_template('CheckTopup.html', authority=authority, user=user, icon=user_icon, islogin=islogined(),
                           check=check)


@app.route('/Confirm/<int:id>', methods=['GET', 'POST'])
def Confirm(id):
    a = CheckMoney.query.filter(CheckMoney.id == id).first()
    user1 = User.query.filter(User.user_name == a.user_name).first()
    a.situation = True
    user1.money = user1.money + a.money
    db.session.commit()
    return redirect(url_for('CheckTopup'))


@app.route('/modify', methods=['GET', 'POST'])
def modify():
    user = User.query.filter(User.user_name == session.get('USERNAME')).first()
    if (user.ban == 1):
        flash('The user has been disabled')
        return redirect(url_for('log_out'))
    user_icon = setIcon()
    authority = session.get('authority')
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
            if user.icon == None:
                file_obj.save(os.path.join(ava_dir, ava_filename))
                user.icon = ava_filename.encode()
            else:
                os.remove(os.path.join(ava_dir, ava_filename))
                file_obj.save(os.path.join(ava_dir, ava_filename))
            flash('AVA uploaded and saved')
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('modify.html', islogin=islogined(), user=user, icon=user_icon, profile=profile, form=form,
                           authority=authority)


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
    if (user_find.ban == 1):
        flash('The user has been disabled')
        return redirect(url_for('login'))
    else:
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
            profile = Profile(user_id=user.id)
            db.session.add(profile)
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
    session.clear()
    return jsonify({'returnValue': 1})
    # session.clear()
    # return redirect('/main_page')

@app.route('/logout', methods=["GET", "POST"])
def log_out():
    session.clear()
    flash('The user has been disabled')
    return redirect(url_for('login'))



@app.route('/main_page')
def main_page():
    if islogined():
        name = session['USERNAME']
        user_icon = setIcon()
        authority = session.get('authority')
    else:
        name = "visitor"
        user_icon = 'NULL'
        authority = 0
    return render_template('index.html', islogin=islogined(), username=name, types=all_type,
                           ype_value=all_type.values(), icon=user_icon, authority=authority)


@app.route('/commodity', methods=['GET', 'POST'])
def get_commodity():
    data = Commodity.query
    commodity = data.order_by(Commodity.release_time)
    authority = session.get('authority')
    return render_template("index.html", commodity=commodity, authority=authority)


# @app.route('/division', methods=['GET', 'POST'])
# def division():
#     return render_template("base.html", types=all_type)


# reset the database
@app.route('/reset_db')
def reset_db():
    set_db()
    return redirect('/')


# Icon
@app.route('/img/<path:filename>')
def get_avatar(filename):
    return send_from_directory((os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/instruments')),
                               filename, as_attachment=True)


# @app.route('/commodity_pic_review')
# def review_pic():
#     c = session['cid']
#     commodity = Commodity.query.filter(Commodity.id == c).first()
#     return render_template('upload_review.html', commodity=commodity)
#
#
# @app.route('/pic1_session_add')
# def add_pic1():
#     session['commodity_pic'] = 1
#     return redirect(url_for('upload'))
#
#
# @app.route('/pic2_session_add')
# def add_pic2():
#     session['commodity_pic'] = 2
#     return redirect(url_for('upload'))
#
#
# @app.route('/pic3_session_add')
# def add_pic3():
#     session['commodity_pic'] = 3
#     return redirect(url_for('upload'))
#
#
# @app.route('/change-commodity/', methods=['GET', 'POST'])
# def upload():
#     if request.method == 'POST':
#         f = request.files.get('file')
#         raw_filename = avatars.save_avatar(f)
#         session['c_filename'] = raw_filename
#         print("../static/instruments/" + session['c_filename'])
#         c = session['cid']
#         commodity = Commodity.query.filter(Commodity.id == c).first()
#         pic_position = session['commodity_pic']
#         if pic_position == 1:
#             commodity.pic_path1 = "../static/instruments/" + session['c_filename']
#         if pic_position == 2:
#             commodity.pic_path2 = "../static/instruments/" + session['c_filename']
#         if pic_position == 3:
#             commodity.pic_path3 = "../static/instruments/" + session['c_filename']
#         db.session.commit()
#         return redirect("/change-commodity/crop/")
#     return render_template('upload.html')
#
#
# @app.route('/change-commodity/crop/', methods=['GET', 'POST'])
# def crop():
#     if request.method == 'POST':
#         x = request.form.get('x')
#         y = request.form.get('y')
#         w = request.form.get('w')
#         h = request.form.get('h')
#         commodity = Commodity.query.filter(Commodity.id == session["cid"]).first()
#         filenames = avatars.crop_avatar(session['c_filename'], x, y, w, h)
#         url_s = filenames[0]
#         url_m = filenames[1]
#         url_l = filenames[2]
#         pic_position = session['commodity_pic']
#         if pic_position == 1:
#             commodity.pic_path1 = "../static/instruments/" + url_l
#         if pic_position == 2:
#             commodity.pic_path2 = "../static/instruments/" + url_l
#         if pic_position == 3:
#             commodity.pic_path3 = "../static/instruments/" + url_l
#         db.session.commit()
#         session.pop('commodity_pic', None)
#         flash('Upload picture successfully', 'success')
#
#         return redirect("/commodity_pic_review")
#     return render_template('crop.html')


# modify commodity page
@app.route('/modify_commodity/<int:id>', methods=['GET', 'POST'])
def modify_single(id):
    if islogined() and session['authority'] == 1:
        # id = session['cid']
        # if request.method == 'POST':
        #     print("modify")
        #     commodity = Commodity.query.get(int(id))
        #     commodity.commodity_name = request.form['product name']
        #     commodity.cargo_quantity = request.form['quantity']
        #     commodity.price = request.form['price']
        #     commodity.introduction = request.form['introduction']
        #     db.session.commit()
        #     return redirect('/commodity_pic_review')
        # else:
        #     print("to start modify")
        #     IsModify = True
        user = User.query.filter(User.user_name == session.get('USERNAME')).first()
        user_icon = setIcon()
        authority = 1
        commodity = Commodity.query.get(int(id))
        if request.method == 'POST':
            commodity.commodity_name = request.form.get('product name')
            commodity.cargo_quantity = request.form.get('quantity')
            commodity.price = request.form.get('price')
            commodity.introduction = request.form.get('introduction')
            commodity.type = request.form.get('type')
            dir = "../static/instruments/"
            if request.files.get('pic1').filename != "":
                f = request.files.get('pic1')
                commodity.pic_path1 = dir + f.filename
                f.save(os.path.join(Config.AVATARS_SAVE_PATH, f.filename))
            if request.files.get('pic2').filename != "":
                f = request.files.get('pic2')
                commodity.pic_path2 = dir + f.filename
                f.save(os.path.join(Config.AVATARS_SAVE_PATH, f.filename))
            if request.files.get('pic3').filename != "":
                f = request.files.get('pic3')
                commodity.pic_path3 = dir + f.filename
                f.save(os.path.join(Config.AVATARS_SAVE_PATH, f.filename))
            if request.files.get('sound').filename != "":
                s = request.files.get('sound')
                s_name = commodity.commodity_name + ".mp3"
                if not os.path.exists(os.path.join(Config.MUSIC_SAVE_PATH, s_name)):
                    os.remove(os.path.join(Config.MUSIC_SAVE_PATH, s_name))
                s.save(os.path.join(Config.MUSIC_SAVE_PATH, s_name))
            db.session.add(commodity)
            db.session.commit()
            session['cid'] = commodity.id
            return redirect(url_for('productList'))
        return render_template('newProduct.html', user=user, icon=user_icon, islogin=islogined(), c=commodity,
                               types=all_type,
                               type_value=all_type.values(), authority=authority, )
    return redirect('/home')


@app.route('/customer', methods=['GET', 'POST'])
def customer():
    user = User.query.filter(User.user_name == session.get('USERNAME')).first()
    user_icon = setIcon()
    authority = session.get('authority')
    if islogined():
        user_icon = setIcon()
        authority = session.get('authority')
    else:
        user_icon = 'NULL'
        authority = 0
    users_id = []
    users_name = []
    users_email = []
    users = User.query.filter(User.authority == 0).all()
    allusers = get_customer(users)
    if request.method == 'POST':
        print("hi")
        # if request.form.get('uid') is not None:
        #     users_id = User.query.filter(User.id == request.form.get('uid')).all()
        #     print(1)
        #     print(users_id)
        # if request.form.get('uname') is not None:
        #     users_name = User.query.filter(User.user_name == request.form.get('uname')).all()
        #     print(2)
        #     print(users_name)
        # if request.form.get('email') is not None:
        #     users_email = User.query.filter(User.email == request.form.get('email')).all()
        #     print(3)
        #     print(users_email)
        # if request.form.get('uid') is None and request.form.get('uname') is None and request.form.get('email') is None:
        #     users = User.query.all()
        #     print(4)
        #     print(users)
        # else:
        #     users = list(set(users_id) & set(users_name) & set(users_email))
        #     print(5)
        #     print(users)
        uid = request.form.get("uid")
        uname = request.form.get("uname")
        email = request.form.get("email")
        filterList = []
        if uid != '':
            filterList.append(User.id == uid)

        if uname != '':
            filterList.append(User.user_name.like('%' + uname + '%'))

        if email != '':
            filterList.append(User.email.like('%' + email + '%'))


        users= User.query.filter(*filterList).all()
        allusers = get_customer(users)

        return render_template('customer.html', islogin=islogined(), authority=authority, allusers=allusers,
                               types=all_type,
                               ype_value=all_type.values(), icon=user_icon, user=user)

    return render_template('customer.html', islogin=islogined(), user=user, authority=authority, allusers=allusers,
                           types=all_type,
                           ype_value=all_type.values(), icon=user_icon)


def get_customer(users):
    allusers = []
    for user in users:
        item = dict()
        item['id'] = user.id
        item['username'] = user.user_name
        item['email'] = user.email
        item['time'] = user.register_time
        item['money'] = user.money
        item['ban'] = user.ban
        allusers.append(item)
    return allusers


@app.route('/productList')
def productList():
    user = User.query.filter(User.user_name == session.get('USERNAME')).first()
    user_icon = setIcon()
    authority = session.get('authority')
    products = Commodity.query.all()
    allproducts = get_product(products)
    return render_template('productList.html', authority=authority, user=user, commodities=allproducts, icon=user_icon,
                           islogin=islogined(),
                           )


def get_product(products):
    allproducts = []
    for p in products:
        item = dict()
        item['id'] = p.id
        item['name'] = p.commodity_name
        item['quantity'] = p.cargo_quantity
        item['time'] = p.release_time
        item['price'] = p.price
        item['type'] = p.type
        allproducts.append(item)
    return allproducts


@app.route('/ban/<int:id>', methods=['GET', 'POST'])
def ban(id):
    user = User.query.filter(User.id == id).first()
    if (user.ban == 0):
        user.ban = 1
    else:
        user.ban = 0
    db.session.commit()
    return redirect(url_for('customer'))
