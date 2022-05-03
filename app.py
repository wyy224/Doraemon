import os
from socket import SocketIO

from flask import Flask

from app import app, db
from app.routes import socketio

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'




if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5002, debug=True)
    # app.run(debug=True)
