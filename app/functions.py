from app.models import *
from flask import session, Flask


# This function is use to reset the database into initialized
def set_db():
    db.drop_all()
    db.create_all()
    from app.models import User, Commodity, Cart, Order, Profile

    # create administrator
    admin = User(user_name='admin', email='admin123@gmail.com', authority=1, icon='admin.jpeg')
    admin.set_password('123456')
    db.session.add(admin)
    profile1 = Profile(user_id=1)
    db.session.add(profile1)

    # create users
    user1 = User(user_name='user1', email='12345678@qq.com', icon='user1_AVA.jpeg', money=10000)
    user1.set_password('000000')
    db.session.add(user1)
    profile2 = Profile(user_id=2)
    db.session.add(profile2)

    user2 = User(user_name='user2', email='87654321@qq.com')
    user2.set_password('111111')
    db.session.add(user2)
    profile3 = Profile(user_id=3)
    db.session.add(profile3)

    user3 = User(user_name='1920', email='135792468@qq.com')
    user3.set_password('222222')
    db.session.add(user3)
    profile4 = Profile(user_id=4)
    db.session.add(profile4)

    rich = User(user_name='rich', email='richrich@gmail.com', money=10000000)
    rich.set_password('666666')
    db.session.add(rich)
    profile5 = Profile(user_id=5)
    db.session.add(profile5)

    # add commodity

    piano = Commodity(commodity_name='piano', cargo_quantity=100, pic_path1='../static/instruments/piano.jpg',
                      price=3000, introduction='This is a piano.', type='piano')
    db.session.add(piano)

    drum = Commodity(commodity_name='drum', cargo_quantity=100,
                     pic_path1='../static/instruments/drum.png',
                     price=3000, introduction='This is a drum.', type='drum')
    db.session.add(drum)

    db.session.commit()

    # add cart
    cart1 = Cart(commodity_id=2, user_id=1, commodity_num=2)

    db.session.add(cart1)

    db.session.commit()

    # add order

    order1 = Order(user_id=2, address='No. 100, Pingyuan Park, Chaoyang District, Beijing', transport='2')

    db.session.add(order1)

    orderD = OrderDetail(commodity_id=1, order_id=1, commodity_num=1)

    db.session.add(orderD)

    db.session.commit()


# This function is use to check whether the user is login
def islogined():
    # Check whether the user is logged into the web
    if session.get('USERNAME'):
        return True
    else:
        return False


def create_app():
    app = Flask(__name__)
