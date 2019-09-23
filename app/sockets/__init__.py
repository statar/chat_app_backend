from flask import Blueprint

chat_socket = Blueprint('main', __name__)

from . import events
