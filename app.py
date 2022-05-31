import os
from socket import SocketIO

from flask import Flask

from app import app, db
from app.routes import socketio
from flask_mail import Mail,Message

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'

app.config['MAIL_DEBUG'] = True
app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'ningxin.li@hotmail.com'
app.config['MAIL_PASSWORD'] = 'PFXT6-PDYTA-LEG2A-QBE2A-AZL6M'
# app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = True

# mail = Mail(app)

def ih():
    return 0;
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5002)
    # app.run(debug=True)
