from data_base import db
from app import create_app
from dotenv import load_dotenv
from blueprints.auth.models import *
from blueprints.projects.models import *

load_dotenv()
app = create_app()
app.app_context().push()
db.drop_all(app=app)
db.create_all(app=app)

Role(name="admin").save()
Role(name="moder").save()
Role(name="user").save()

org = Organization(name="ЭКЦ")
user = User(
    email='testuser@gmail.com',
    password='12345678',
    name='Testuser',
    surname='Testuser'
)
user.org = org
user_role = UserRole(role_id=Role.find_user_id())
user_role.user = user
user.save()
