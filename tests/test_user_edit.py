from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

class TestUserEdit(BaseCase):

    def register(self):
        register_data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        register_data.update(
            {"id": self.get_json_value(response, "id")}
        )
        return register_data

    def login(self, login_data):
        response = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")
        return auth_sid, token

    def test_edit_just_create_user(self):
        # register
        register_data = self.prepare_registration_data()

        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # login
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # edit
        new_name = "Changed name"
        response3 = MyRequests.put(f"/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"firstName": new_name})

        Assertions.assert_code_status(response3, 200)

        # get
        response4 = MyRequests.get(f"/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

#   Попытаемся изменить данные пользователя, будучи неавторизованными
    def test_edit_not_auth(self):
        user = self.register()

        new_name = "Changed name"

        response = MyRequests.put(f"/user/{user['id']}",
                                data={"firstName": new_name})

        Assertions.assert_code_status(response, 400)
        assert response.json()['error'] == 'Auth token not supplied', \
            f"Unexpected response result {response.content}"

    def test_edit_other_user(self):
        user1 = self.register()
        user2 = self.register()

        auth_sid, token = self.login(user1)

        new_name = "Changed name"

        response = MyRequests.put(f"/user/{user2['id']}",
                                  headers={"x-csrf-token": token},
                                  cookies={"auth_sid": auth_sid},
                                  data={"username": new_name})

        #Assertions.assert_code_status(response, 400)

        response2 = MyRequests.get(f"/user/{user2['id']}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )

        Assertions.assert_json_value_by_name(response2, "username", user2['username'], "Wrong name of user after edit")

# - Попытаемся изменить email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @
    def test_edit_incorrect_email(self):
        user = self.register()

        auth_sid, token = self.login(user)

        new_email = "ivanovadot.com"
        response = MyRequests.put(f"/user/{user['id']}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"email": new_email})

        Assertions.assert_code_status(response, 400)
        assert response.json()['error'] == 'Invalid email format', \
            f"Unexpected response result {response.content}"

        response2 = MyRequests.get(f"/user/{user['id']}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid}
                                   )

        Assertions.assert_json_value_by_name(response2, 'email', user['email'],
                                             f"email has been changed to an invalid email: {new_email}")

    # - Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем, на очень короткое значение в один символ
    def test_edit_short_name(self):
        user = self.register()

        auth_sid, token = self.login(user)

        new_firstname = "Y"
        response = MyRequests.put(f"/user/{user['id']}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_firstname})

        Assertions.assert_code_status(response, 400)
        assert response.json()['error'] == 'The value for field `firstName` is too short', \
            f"Unexpected response result {response.content}"

        response2 = MyRequests.get(f"/user/{user['id']}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid}
                                   )

        Assertions.assert_json_value_by_name(response2, 'firstName', user['firstName'],
                                             f"firstnamehas been changed to an invalid name: {new_firstname}")




