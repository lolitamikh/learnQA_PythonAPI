from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

class TestUserDelete(BaseCase):
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

    def test_delete_user_default(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        auth_sid, token = self.login(data)

        response = MyRequests.delete("/user/2",
                                     headers={'x-csrf-token': token},
                                     cookies={'auth_sid': auth_sid})

        Assertions.assert_code_status(response, 400)
        assert response.json()['error'] == 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.', \
            f"Unexpected response result {response.content}"

    def test_user_delete_succesed(self):
        user = self.register()

        auth_sid, token = self.login(user)

        response = MyRequests.delete(f"/user/{user['id']}",
                                     headers={'x-csrf-token': token},
                                     cookies={'auth_sid': auth_sid})

        Assertions.assert_code_status(response, 200)

        response2 = MyRequests.get(f"/user/{user['id']}'",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )

        Assertions.assert_code_status(response2, 404)
        assert response2.content.decode("utf-8") == f"This is 404 error!\n<a href='/'>Home</a>", \
            f"Unexpected response content: {response2.content}"

    def test_delete_other_user(self):
        user1 = self.register()
        user2 = self.register()

        auth_sid, token = self.login(user1)

        response = MyRequests.delete(f"/user/{user2['id']}",
                                     headers={'x-csrf-token': token},
                                     cookies={'auth_sid': auth_sid})

        response2 = MyRequests.get(f"/user/{user1['id']}'",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )

        #Assertions.assert_json_value_by_name(response2, "username", user2['username'], "User was deleted but shouldn't")





