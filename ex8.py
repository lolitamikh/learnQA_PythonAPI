import requests
import json
import time

def request(token):
    params = {'token': token}
    url = "https://playground.learnqa.ru/ajax/api/longtime_job"
    response = requests.get(url, params=params)
    print(response.url)
    print(response.text)
    return response.text

def json_text(req, key):
    jsons = json.loads(req)
    try:
        keys = jsons[key]
        return keys
    except:
        return None

req1 = request(token=None)
tokens = json_text(req1, "token")
times = json_text(req1, 'seconds')

req2 = request(tokens)
status = json_text(req2, "status")
result = json_text(req2, "result")

if status == 'Job is NOT ready':
    print('задача не готова ждемс')
    time.sleep(times)
    req3 = request(tokens)
    status = json_text(req3, "status")
    result = json_text(req3, "result")
    if status == 'Job is ready' and result == '42':
        print('задача готова')