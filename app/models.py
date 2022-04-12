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
    icon = db.Column(db.String(128), nullable=True)
    introduction = db.Column(db.String(64), nullable=True)
    authority = db.Column(db.Integer, default=0, nullable=False)
    money = db.Column(db.Integer, default=0, nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.user_name)

    # encrypt password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # translate password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# A table of ranking list
class Commodity(db.Model):
    __tablename__ = "commodity"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    commodity_name = db.Column(db.String(32), nullable=False)
    release_time = db.Column(db.DateTime, default=datetime.now)
    cargo_quantity = db.Column(db.Integer, nullable=False)
    pic_path = db.Column(db.String(64), nullable=True)
    price = db.Column(db.Integer, nullable=False)
    introduction = db.Column(db.String(64), nullable=True)
    type = db.Column(db.String(32), nullable=False)
    is_collect = db.Column(db.Boolean, default=False, nullable=False)



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
    transport = db.Column(db.String(64),nullable=False)
    is_receive = db.Column(db.Boolean, default=False, nullable=False)

# A table of order detail
class OrderDetail(db.Model):
        __tablename__ = "orderdetail"
        __table_args__ = {'extend_existing': True}
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        commodity_id = db.Column(db.Integer, db.ForeignKey('commodity.id'))
        order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
        commodity_num = db.Column(db.Integer, default=0, nullable=False)

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