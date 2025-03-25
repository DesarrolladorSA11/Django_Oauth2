import requests
from decouple import config

url = "http://127.0.0.1:8000/o/token/"

print("CLIENT_ID", config("CLIENT_ID"))
print("CLIENT_SECRET", config("CLIENT_SECRET"))

data = {
    "client_id": config("CLIENT_ID"),
    "client_secret": config("CLIENT_SECRET"),
    "code": "kSeZaMMYDep4U1fLkSvTw4YlmTpTni",
    "code_verifier": "3QE4LKUL19HBPKWUWZ64LVLQMLB1WL0ANSZXUDWM8IFPRSMLATO961MFKA62CT9YCZSNY1A19JNU76MIMGH6PS10GAMJIL6GTQT12L9E7ERYGUHQJ",
    "redirect_uri": "http://127.0.0.1:8000/noexist/callback",
    "grant_type": "authorization_code",
}

response = requests.post(url, data=data)
print(response.json())
