import os
from socket import SocketIO

from flask import Flask

from app import app, db

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'

socketio = SocketIO()
socketio.init_app(app)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    # app.run(debug=True)
