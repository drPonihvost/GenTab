import os

from base.data_base import db
from app import create_app
from dotenv import load_dotenv

load_dotenv()
db.drop_all(app=create_app())
db.create_all(app=create_app())
