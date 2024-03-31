import requests

class TestHeaders:
    def test_headers(self):
        url = "https://playground.learnqa.ru/api/homework_header"
        response = requests.get(url)
        print(response.headers)
        headers = response.headers
        assert 'x-secret-homework-header' in headers, "There are no such headers in response"
        assert 'Some secret value' in headers.values(), "There are no such headers values in response"