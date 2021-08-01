import requests
from app import create_app

app = create_app()

payload = {'email': 'testuser@gmail.com', 'password': '12345678'}

class TestAPI:
    def setup(self):
        app.testing = True
        self.client = app.test_client()

    def test_example_1(self):
        self.token = self.client.post(
            '/token',
            json=payload
        )
        print(self.token)

    def test_example_2(self):
        assert 1 + 1 == 2

    def teardown(self):
        pass

x = TestAPI()
x.setup()
x.test_example_1()






# payload = {'email': 'testuser@gmail.com', 'password': '12345678'}
#
# def autenticate(payload):
#     url = 'http://127.0.0.1:5000/token'
#     response = requests.post(url, json=payload)
#     token = response.json().get("access_token")
#     return response
#
# def test_autenticate():
#     assert autenticate(payload).status_code == 200
#
# def upload():
#     url = 'http://127.0.0.1:5000/upload'
#     token = autenticate(payload).json().get("access_token")
#     file = {'file': open('../test projects/test_partial_valid.txt')}
#     response = requests.post(url, files=file, headers={"Authorization": f"Bearer {token}"})
#     return response
#
# def test_upload():
#     assert upload().status_code == 400


# url = 'http://127.0.0.1:5000/projects/'
# response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
# print(response.status_code)
# print(response.text)
