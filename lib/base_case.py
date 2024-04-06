import json.decoder
from requests import Response

class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Cannot find cookie with {cookie_name} on the last response"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, header_name):
        assert header_name in response.cookies, f"Cannot find header with {header_name} on the last response"
        return response.headers[header_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecoder:
            assert False, f"Response is not JSON Format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON doesn't have key'{name}'"

        return response_as_dict[name]