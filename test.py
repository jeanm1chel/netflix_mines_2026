import requests


url = "http://localhost:8000/auth/login"

user = {
    "email": "mauvais@test.com",
    "pseudo": "michel",
    "password": "mauvais_password"
}

response = requests.post(url, json=user)
print(response.status_code)
print(response.json())