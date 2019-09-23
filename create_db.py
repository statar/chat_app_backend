#!env/bin/python

from app import app, db
from app.database import models
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

engine = create_engine("postgres://postgres:1numan1@localhost/web_chat_task")
if not database_exists(engine.url):
    create_database(engine.url)

print(database_exists(engine.url))

db.drop_all()
db.create_all()
