from flask import session, request
from flask_socketio import emit, send, join_room, leave_room
from .. import socketio
from .. import database

actions = { "JOINED": 0, "LEFT":1, "RENAME":2 }

@socketio.on('user_action')
def action_handler(user_connected):
    user_action = actions['LEFT']
    user_action_obj = database.UserActionInterface(session['user_id'])
    # Save user login information in action table
    if (user_connected):
        user_action = actions['JOINED']
        user_action_obj.save_new_login()
    # Logout user from user action table in database
    else:
        user_action_obj.log_out_user()
    emit('user_action', {'user': user_action_obj.get_user_info(), 'action': user_action}, broadcast=True)

@socketio.on('connect')
def on_connect():
    if(request.args.get('user_id') is not None): # Client should provide user_id
        session['user_id'] = request.args.get('user_id')
        action_handler(user_connected = True)

@socketio.on('disconnect')
def on_dısconnect():
    action_handler(user_connected = False)

@socketio.on('message')
def handle_message(message):
    emit('message',message, broadcast=True)

