# src/database/user_login_rest.py

from flask import Flask, request, make_response, jsonify
from flask_httpauth import HTTPTokenAuth

from app import app, db
from app.database.models.user import User, BlacklistToken
from app.database.models_schema.user_schema import UserSchema

token_auth = HTTPTokenAuth('Token')

url_prefix = app.config.get('REST_URL_PREFIX')
test_token = app.config.get('TEST_TOKEN')

@token_auth.verify_token
def verify_token(token):
    """ Verify user token """
    resp = User.decode_auth_token(token)
    if not isinstance(resp, str):
        user = User.query.filter_by(user_id=resp).first()
        if user:
            return True
    return False

# User login
@app.route(url_prefix + '/auth/login', methods=['POST'])
def login_api():
    # get the post data
    post_data = request.get_json()
    # fetch the user data
    user = User.query.filter_by(email=post_data.get('user_mail')).first()
    if (user):
        pwd_valid = user.validate_password(post_data.get('user_password'))
        if pwd_valid:
            # Update login flag if user name and password are correct
            user.logged_in = True
            db.session.merge(user)
            db.session.commit()
            # Create auth token if user name and password are correct
            auth_token = user.encode_auth_token(user.user_id)
            if auth_token:
                responseObject = {
                    'status': 'Success',
                    'message': 'Successfully logged in.',
                    'auth_token': auth_token.decode()
                }
                print(responseObject)
                return make_response(jsonify(responseObject)), 200
    responseObject = {
        'status': 'Fail',
        'message': 'Email address or password is not correct!'
    }
    print(responseObject)
    return make_response(jsonify(responseObject)), 203

# User status and check if logged in
@app.route(url_prefix + '/auth/status', methods=['GET'])
@token_auth.login_required
def user_api():
    # get the auth token
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except IndexError:
            responseObject = {
                'status': 'Fail',
                'message': 'Bearer token malformed.'
            }
            return make_response(jsonify(responseObject)), 401
    if auth_token:
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            user = User.query.filter_by(user_id=resp).first()
            result = UserSchema().dump(user, many=False)
            return make_response(jsonify(result)), 200
        responseObject = {
            'status': 'Fail',
            'message': resp
        }
        return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            'status': 'Fail',
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(responseObject)), 403

# User logout
@app.route(url_prefix + '/auth/logout', methods=['GET'])
@token_auth.login_required
def logout_api():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except IndexError:
            responseObject = {
                'status': 'Fail',
                'message': 'Bearer token malformed.'
            }
            return make_response(jsonify(responseObject)), 401
    if auth_token:
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            user = User.query.filter_by(user_id=resp).first()
            # Update login flag
            user.logged_in = False
            db.session.merge(user)
            db.session.commit()
            # mark the token as blacklisted
            blacklist_token = BlacklistToken(token=auth_token)
            try:
                # insert the token
                db.session.add(blacklist_token)
                db.session.commit()
                responseObject = {
                    'status': 'Success',
                    'message': 'Successfully logged out.'
                }
                return make_response(jsonify(responseObject)), 200
            except Exception as e:
                responseObject = {
                    'status': 'Fail',
                    'message': e
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'Fail',
                'message': resp
            }
            return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            'status': 'Fail',
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(responseObject)), 403
