# Необходимо написать тест, который делает запрос на метод: https://playground.learnqa.ru/api/homework_cookie Этот
# метод возвращает какую-то cookie с каким-то значением. Необходимо с помощью функции print() понять что за cookie и
# с каким значением, и зафиксировать это поведение с помощью assert
import requests

class TestCookie:
    def test_cookie(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"
        response = requests.get(url)
        print(response.cookies)
        cookies = response.cookies
        assert "HomeWork" in cookies, "There is no cookies name in response"
        assert "hw_value" in cookies.values(), "There is no cookies in response"