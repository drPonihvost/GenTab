from data_base import db
from app import create_app
from dotenv import load_dotenv
from blueprints.auth.models import *
from blueprints.projects.models import *

load_dotenv()
db.drop_all(app=create_app())
db.create_all(app=create_app())
