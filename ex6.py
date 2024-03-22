import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")

for i, val in enumerate(response.history, start=1):
    print(f'{i} {val.status_code} {val.url}')

