from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


# A table of users in database
class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}
    # information
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(32), unique=True, nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    register_time = db.Column(db.DateTime, default=datetime.now)
    gender = db.Column(db.String(10), nullable=True)
    icon = db.Column(db.String(128), default='default.jpeg')
    introduction = db.Column(db.String(64), nullable=True)
    authority = db.Column(db.Integer, default=0, nullable=False)
    money = db.Column(db.Integer, default=0, nullable=False)
    new_time = db.Column(db.DateTime, nullable=True)
    count = db.Column(db.Integer, default=0)
    situation = db.Column(db.Boolean, nullable=True)
    messages = db.relationship('Mess', back_populates='author', cascade='all')
    ban = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User {}>'.format(self.user_name)

    # encrypt password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # translate password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# A table of message list
class Mess(db.Model):
    __tablename__ = "message"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    room = db.Column(db.String(64), nullable=False)
    read = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime, default=datetime.now, index=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_name = db.Column(db.String(64), nullable=False)
    author = db.relationship('User', back_populates='messages')


# A table of ranking list
class Commodity(db.Model):
    __tablename__ = "commodity"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    commodity_name = db.Column(db.String(32), nullable=False)
    name_zh = db.Column(db.String(32), nullable=False)
    release_time = db.Column(db.DateTime, default=datetime.now)
    cargo_quantity = db.Column(db.Integer, nullable=False)
    pic_path1 = db.Column(db.String(64), nullable=True)
    pic_path2 = db.Column(db.String(64), nullable=True)
    pic_path3 = db.Column(db.String(64), nullable=True)
    price = db.Column(db.Integer, nullable=False)
    introduction = db.Column(db.String(64), nullable=True)
    intro_zh = db.Column(db.String(64), nullable=True)
    type = db.Column(db.String(32), nullable=False)
    collect_num = db.Column(db.Integer, default=0)
    is_collect = db.Column(db.Boolean, default=False, nullable=False)
    is_delete = db.Column(db.Boolean, default=False, nullable=False)


# A table of shopping cart
class Cart(db.Model):
    __tablename__ = "cart"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    commodity_id = db.Column(db.Integer, db.ForeignKey('commodity.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    add_time = db.Column(db.DateTime, default=datetime.now)
    commodity_num = db.Column(db.Integer, default=1, nullable=False)


# A table of order form
class Order(db.Model):
    __tablename__ = "order"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    purchase_time = db.Column(db.DateTime, default=datetime.now)
    address = db.Column(db.String(64), nullable=False)
    transport = db.Column(db.String(64), nullable=False)
    status = db.Column(db.String(64), default='Not deliver', nullable=False)
    phone_num = db.Column(db.String(11), nullable=True)
    name = db.Column(db.String(11), nullable=True)
    Urgent = db.Column(db.Boolean, default=False, nullable=False)



# A table of order detail
class OrderDetail(db.Model):
    __tablename__ = "orderdetail"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    commodity_id = db.Column(db.Integer, db.ForeignKey('commodity.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    commodity_num = db.Column(db.Integer, default=0, nullable=False)

class CheckMoney(db.Model):
    __tablename__ = "checkmoney"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(32), db.ForeignKey('user.user_name'))
    time = db.Column(db.DateTime, default=datetime.now)
    money = db.Column(db.Integer, default=0, nullable=False)
    situation = db.Column(db.Boolean, default=False, nullable=False)




# A table of more user information
class Profile(db.Model):
    __tablename__ = "profile"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    address = db.Column(db.String(64), nullable=True)
    phone_num = db.Column(db.String(11), nullable=True)
    name = db.Column(db.String(11), nullable=True)


# A table of collection list
class Collections(db.Model):
    __tablename__ = "collections"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    commodity_id = db.Column(db.Integer, db.ForeignKey('commodity.id'))
    commodity = db.relationship('Commodity', backref=db.backref('Commodity', lazy='dynamic'))


# A table of review
class Review(db.Model):
    __tablename__ = "review"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    commodity_id = db.Column(db.Integer, db.ForeignKey('commodity.id'))
    title = db.Column(db.String(32), nullable=False)
    text = db.Column(db.String(128), nullable=False)
    created = db.Column(db.DateTime, default=datetime.now)

# # A table of review
# class Review(db.Model):
#     __tablename__ = "review"
#     __table_args__ = {'extend_existing': True}
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     commodity_id = db.Column(db.Integer, db.ForeignKey('commodity.id'))
#     title = db.Column(db.String(32), nullable=False)
#     text = db.Column(db.String(128), nullable=False)
#     created = db.Column(db.DateTime, default=datetime.now)
