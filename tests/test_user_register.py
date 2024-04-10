from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import pytest
import random
import string
import allure

@allure.epic("Cases user create")
class TestUserRegister(BaseCase):
    params = [
        ('password'),
        ('username'),
        ('firstName'),
        ('lastName'),
        ('email')
    ]

    @allure.description("This test create user")
    @allure.label("happy path")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.description("This test create user with existing email")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    @allure.description("This test create user with incorrect email")
    def test_create_user_with_incorrect_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"Invalid email format", f"Unexpected response content {response.content}"

    @allure.description("This test create user with missing arguments")
    @pytest.mark.parametrize('param', params)
    def test_null_param(self, param):
        data = self.prepare_registration_data()
        data[param] = None

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"The following required params are missed: {param}", f"Unexpected response content {response.content}"

    @allure.description("This test create user with short first name")
    def test_create_user_short_firstname(self):
        data = self.prepare_registration_data()
        data['firstName'] = "".join([random.choice(string.ascii_letters) for i in range(random.randrange(2))])

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"The value of 'firstName' field is too short", f"Unexpected response content {response.content}"

    @allure.description("This test create user with long first name")
    def test_create_user_long_firstname(self):
        data = self.prepare_registration_data()
        data['firstName'] = "".join([random.choice(string.ascii_letters) for i in range(random.randrange(500))])

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"The value of 'firstName' field is too long", f"Unexpected response content {response.content}"
