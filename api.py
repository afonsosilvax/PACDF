import requests

API_key = '463198d01a64c66d6a4653bc5cad3f42df7bfc73'
url = f'https://api.radarbox.com/v2/airports/LGW&api_key={API_key}'

headers = {"Accept": "application/json; charset=UTF-8"}

resposta = requests.get(url, headers=headers)

print(resposta.status_code)
print(resposta.json())