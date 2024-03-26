import requests

response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(f' 1 {response.text}')

response = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": "HEAD"})
print(f' 2 {response.text}')

response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": "POST"})
print(f' 3 {response.text}')
print("")

method = {"get": "GET",
          "put": "PUT",
          "post": "POST",
          "delete": "DELETE"}

for key in method:
    payload = {"method": method[key]}
    response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data=payload)
    print(f' POST-{method[key]} {response.text}')
    response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=payload)
    print(f' GET-{method[key]} {response.text}')
    response = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data=payload)
    print(f' PUT-{method[key]} {response.text}')
    response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data=payload)
    print(f' DELETE-{method[key]} {response.text}')
    print('')





