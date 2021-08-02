import requests
from flask import json, jsonify
from app import create_app
from base.data_base import db
from dotenv import load_dotenv
from blueprints.auth.models import *
from blueprints.projects.models import *


load_dotenv()
app = create_app(test=True)
app.testing = True

client = app.test_client()

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

payload = {'email': 'testuser@gmail.com', 'password': '12345678'}


# class TestAPI:
#     def setup(self):
#         app.testing = True
#         self.client = app.test_client()
#
#
#     def test_example_1(self):
#         token = self.client.get(
#             '/token',
#             json={
#                 "email": "testuser@gmail.com",
#                 "password": "12345678"
#             }
#         )
#         assert token.status_code == 200
#
#     def test_example_2(self):
#         assert 1 + 1 == 2
#
#     def teardown(self):
#         pass

token = client.get(
            '/token',
            json={
                "email": "testuser@gmail.com",
                "password": "12345678"
            }
        )
data = json.loads(token.data)
print(data)
token = token.get_json()
token = token['access_token']

file = {'file': open('test projects/test_partial_valid.txt')}
upload = client.post('/upload', data={'file': open('test projects/test_partial_valid.txt')}, headers={"Authorization": f"Bearer {token}"})

projects = client.get('/projects/', headers={"Authorization": f"Bearer {token}"})
print(projects.get_json())







# payload = {'email': 'testuser@gmail.com', 'password': '12345678'}
#
# def autenticate(payload):
#     url = 'http://127.0.0.1:5000/token'
#     response = requests.get(url, json=payload)
#     token = response.json().get("access_token")
#     return response
#
# def test_autenticate():
#     assert autenticate(payload).status_code == 200
#
# def upload():
#     url = 'http://127.0.0.1:5000/upload'
#     token = autenticate(payload).json().get("access_token")
#     file = {'file': open('test projects/test_partial_valid.txt')}
#     response = requests.post(url, files=file, headers={"Authorization": f"Bearer {token}"})
#     return response
#
# def test_upload():
#     assert upload().status_code == 400
#

# url = 'http://127.0.0.1:5000/projects/'
# response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
# print(response.status_code)
# print(response.text)
