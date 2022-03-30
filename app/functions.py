from app.models import *
from flask import session


# This function is use to reset the database into initialized
def set_db():
    db.drop_all()
    db.create_all()
    from app.models import User, Commodity, Cart, Order, Profile

    # create administrator
    admin = User(user_name='admin', email='admin123@gmail.com', authority=1)
    admin.set_password('123456')
    db.session.add(admin)
    profile1 = Profile(user_id=1)
    db.session.add(profile1)

    # create users
    user1 = User(user_name='user1', email='12345678@qq.com', icon='82f58fa4a973419d9a997abb07ad02fd_l.png')
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


    # add commodity

    piano = Commodity(commodity_name='piano', cargo_quantity=100, pic_path='../static/instruments/piano.jpg',
                      price=3000, introduction='piano', type='piano')
    db.session.add(piano)

    drum = Commodity(commodity_name='drum', cargo_quantity=100, pic_path='../static/instruments/drumps.jpg',
                     price=3000, introduction='drum', type='drum')
    db.session.add(drum)

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
