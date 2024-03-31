import requests

class TestCookie:
    def test_cookie(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"
        response = requests.get(url)
        print(response.cookies)
        cookies = response.cookies
        assert "HomeWork" in cookies, "There is no cookies name in response"
        assert "hw_value" in cookies.values(), "There is no cookies in response"