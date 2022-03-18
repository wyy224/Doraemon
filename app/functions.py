from app.models import *
from flask import session


# This function is use to reset the database into initialized
def set_db():
    db.drop_all()
    db.create_all()
    from app.models import User, Commodity, Cart, Order

    # create user1
    # user1 = User(user_name = 'user1', email = '12345678@qq.com')
    # user1.set_password('000000')
    # db.session.add(user1)
    #
    # user2 = User(user_name='user2', email = '87654321@qq.com')
    # user2.set_password('111111')
    # db.session.add(user2)
    #
    # user3 = User(user_name='1920', email = '135792468@qq.com')
    # user3.set_password('222222')
    # db.session.add(user3)

    # add commodity

    piano = Commodity(commodity_name='piano', cargo_quantity=100, pic_path='../static/instruments/piano.jpg',
                      price=3000, introduction='piano', type='piano')
    db.session.add(piano)

    db.session.commit()


# This function is use to check whether the user is login
def islogined():
    # Check whether the user is logged into the web
    if session.get('USERNAME'):
        return True
    else:
        return False
