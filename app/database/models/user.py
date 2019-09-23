# src/database/models/user.py

import jwt
import datetime
import hashlib
import bcrypt
import codecs

from app import app, db

class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "UserAccount"

    user_id              = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_name            = db.Column(db.String(225), unique=True, nullable=False)
    email                = db.Column(db.String(225), unique=True)
    password             = db.Column(db.String(225), nullable=False)
    age                  = db.Column(db.Integer, nullable=True)
    city                 = db.Column(db.String(225), nullable=True)
    logged_in            = db.Column(db.Boolean, default=False)

    def __init__(self, user_name, email, password, age, city):
        self.user_name = user_name
        self.email     = email
        self.password  = self.create_password(password) # Generate hashed password
        self.age       = age
        self.city      = city
        self.logged_in = False

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    days=0, seconds=app.config.get('TOKEN_VAILD_SEC')),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            print(e)
            return e

    def create_password(self, password):
        """Function to create PBKDF2 encrypted string for given password and random salt."""
        salt = bcrypt.gensalt().split(b'$')[-1] # All text will be like this $2a$10$vI8aWBnW3fID.ZQ4/zo1G.q1lRps.9cGLcZEiGDMVr5yUP1KUOYTa
        passwd_hash = self.create_password_hash(password, salt)
        return 'PBKDF2${}${}${}'.format(
            app.config.get('HASH_FUNCTION'),
            salt.decode('utf-8'),
            passwd_hash
        )

    def create_password_hash(self, password, salt):
        """Function to create hash for given password and salt."""
        if isinstance(password, str):
            password = password.encode('utf-8')
        if isinstance(salt, str):
            salt = salt.encode('utf-8')
        passwd_hash = hashlib.pbkdf2_hmac(
            app.config.get('HASH_FUNCTION'),
            password,
            salt,
            app.config.get('COST_FACTOR'),
            app.config.get('KEY_LENGTH')
        )
        return codecs.encode(passwd_hash, 'hex_codec').decode("utf-8")

    def validate_password(self, password):
        """Check a password against an existing hash."""
        pwd_split = self.password.split('$')
        salt, stored_hash = pwd_split[-2:]
        verfify_hash = self.create_password_hash(password, salt)
        return verfify_hash == stored_hash

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), True, 'HS256')
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'BlacklistTokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False
