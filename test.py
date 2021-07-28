import requests

payload = {'email': 'user@gmail.com', 'password': '12345678'}

url = 'http://127.0.0.1:5000/token'
response = requests.post(url, json=payload)
token = response.json().get("access_token")

url = 'http://127.0.0.1:5000/upload'
file = {'file': open('test projects/test_partial_valid.txt')}
response = requests.post(url, files=file, headers={"Authorization": f"Bearer {token}"})
print(response.status_code)
print(response.text)

# url = 'http://127.0.0.1:5000/projects/'
# response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
# print(response.status_code)
# print(response.text)
