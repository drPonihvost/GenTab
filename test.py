import requests

payload = {'email': 'testuser@gmail.com', 'password': '12345678'}

def autenticate(payload):
    url = 'http://127.0.0.1:5000/token'
    response = requests.post(url, json=payload)
    token = response.json().get("access_token")
    return response

def test_autenticate():
    assert autenticate(payload).status_code == 200

def upload():
    url = 'http://127.0.0.1:5000/upload'
    token = autenticate(payload).json().get("access_token")
    file = {'file': open('test projects/test_partial_valid.txt')}
    response = requests.post(url, files=file, headers={"Authorization": f"Bearer {token}"})
    return response

def test_upload():
    assert upload().status_code == 400


# url = 'http://127.0.0.1:5000/projects/'
# response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
# print(response.status_code)
# print(response.text)
