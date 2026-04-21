import requests

BASE_URL = "http://localhost:8000"

response = requests.post(f"{BASE_URL}/auth/register", json={
    "email": "nouveau@test.com",
    "pseudo": "nouveauUser",
    "password": "password123"
})

print(response.status_code)
print(response.json())