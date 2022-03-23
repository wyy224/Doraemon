from flask import Flask
from flask_avatars import Avatars

from app.config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
db.init_app(app)
avatars = Avatars()
avatars.init_app(app)

from app import routes, models