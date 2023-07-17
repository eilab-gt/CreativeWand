"""
RemoteAPI.py

includes utilities to call a REST API.
"""
import json
import requests


class Response:
    """
    Response object for Remote APIs.
    """

    def __init__(self, success: bool = False, payload=None):
        """
        Initialize this response.
        :param success: Whether the operation had succeeded.
        :param payload: The information in the response.
        """
        self.success = success
        self.payload = payload


class RemoteAPIInterface():
    """
    Interface for REST API.
    """

    @staticmethod
    def request(
            method: str = "POST",
            address: str = None,
            data: dict = None,
    ) -> Response:
        """
        Call a REST API using the data dictionary as payload.
        :param method: (GET/POST) method to use.
        :param address: URL address of the API.
        :param data: data payload.
        :return: Response.
        """

        # Stub
        if method == "POST":
            try:
                result = RemoteAPIInterface.post_request(url=address, data=data, max_retries=10)
                return Response(True, result)
            except Exception as e:
                return Response(False, str(e))
        elif method == "GET":
            try:
                result = RemoteAPIInterface.get_request(url=address, data=data, max_retries=10)
                return Response(True, result)
            except Exception as e:
                return Response(False, str(e))

        return Response(False, None)

    @staticmethod
    def post_request(url, data, max_retries=-1):
        # print("DATA = %s"%data)
        retries = 0
        if type(data) is dict or type(data) is list:
            data = json.dumps(data)
        while True:
            try:
                r = requests.post(url=url, data=data)
                # print(r.text)
                result = json.loads(r.text)
                # print("RESULT:%s"%r.text)
                return result
            except Exception as e:
                retries += 1
                if 0 < max_retries <= retries:
                    print("Exception in post request: %s:%s. Max retries reached." % (str(type(e)), str(e)))
                    raise e

    @staticmethod
    def get_request(url, data=None, max_retries=-1):
        if data is None:
            data = {}
        retries = 0
        # print("DATA = %s"%data)
        if type(data) is dict:
            data = json.dumps(data)
        while True:
            try:
                r = requests.get(url=url, params=data)
                result = json.loads(r.text)
                # print("RESULT:%s"%r.text)
                return result
            except Exception as e:
                retries += 1
                if 0 < max_retries <= retries:
                    print("Exception in get request: %s. Max retries reached." % str(e))
                    raise e
