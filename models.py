from app.__init__ import db
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
    register_time = db.Column(db.DateTime, default=datetime.now)
    gender = db.Column(db.String(10), nullable=True)
    pic_path = db.Column(db.String(64), nullable=True)
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
    step = db.Column(db.Integer, nullable=False)
    cargo_quantity = db.Column(db.Integer, nullable=False)
    pic_path = db.Column(db.String(64), nullable=True)
    price = db.Column(db.Integer, nullable=False)
    introduction = db.Column(db.String(64), nullable=True)


# A table of shopping cart
class Cart(db.Model):
    __tablename__ = "cart"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    commodity_id = db.Column(db.Integer, db.Foreignkey('commodity.id'))
    user_id = db.Column(db.Integer, db.Foreignkey('user.id'))
    add_time = db.Column(db.DateTime, default=datetime.now)
    commodity_num = db.Column(db.Integer, default=1, nullable=False)


# A table of order form
class Order(db.Model):
    __tablename__ = "order"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    commodity_id = db.Column(db.Integer, db.Foreignkey('commodity.id'))
    user_id = db.Column(db.Integer, db.Foreignkey('user.id'))
    purchase_time = db.Column(db.DateTime, default=datetime.now)
    commodity_num = db.Column(db.Integer, default=0, nullable=False)
    address = db.Column(db.String(64), nullable=False)
    transport = db.Column(db.String(64),nullable=False)