import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_socketio import SocketIO
from flask_cors import CORS

socketio = SocketIO()

"""Create an application."""
app = Flask(__name__)

CORS(app)
# set application wide configuration parameters
app_settings = os.getenv(
    'APP_SETTINGS',
    'config.DevelopmentConfig'
)
app.config.from_object(app_settings)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

from .database import *
from .sockets import chat_socket as main_blueprint
app.register_blueprint(main_blueprint)

socketio.init_app(app)



