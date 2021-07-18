from data_base import db
from app import create_app
from dotenv import load_dotenv
from blueprints.auth.models import *
from blueprints.projects.models import *

load_dotenv()
app = create_app()
app.app_context().push()
db.drop_all(app=create_app())
db.create_all(app=create_app())

Role(name="admin").save()
Role(name="moder").save()
Role(name="user").save()
