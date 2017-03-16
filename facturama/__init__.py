#!/usr/bin/python
# coding: utf-8
# (c) 2017 Raul Granados <@pollitux>

from requests import post, get, patch, put, delete

try:
    import json
except ImportError:
    import simplejson as json

__version__ = '0.0.1'
__author__ = 'Raul Granados'

_credentials = ('', '')

API_BASE = 'https://www.facturama.mx/api/'


class FacturamaError(Exception):
    def __init__(self, error_json):
        super(FacturamaError, self).__init__(error_json)
        self.error_json = error_json


class MalformedRequestError(FacturamaError): pass


class AuthenticationError(FacturamaError): pass


class ProcessingError(FacturamaError): pass


class ResourceNotFoundError(FacturamaError): pass


class ParameterValidationError(FacturamaError): pass


class ApiError(FacturamaError): pass


class Facturama:
    def __init__(self):
        self._username, self._password = _credentials
        self._headers = {'content-type': 'application/json'}
        self.auth_api()

    def auth_api(self):
        """
        Login in the api
        :return:
        """
        payload = {
            'username': self._username,
            'password': self._password,
            'grant_type': 'password'
        }

        body = post('{}{}'.format(API_BASE, 'LogIn'), data=json.dumps(payload))


        if body.status_code == 400 or body.status_code == 400:
            raise MalformedRequestError(json.loads(body))
        elif body.status_code == 401 or body.status_code == 401:
            raise AuthenticationError(json.loads(body))
        elif body.status_code == 404 or body.status_code == 404:
            raise AuthenticationError(json.loads(body))
        print(vars(body), 'sdsdd')
        auth = body.json()
        self._headers = {'Authorization': 'Bearer {}'.format(auth['access_token']), 'content-type': 'application/json'}

    def build_http_request(self, method, path, payload=None):

        method = str(method).lower()
        if method == 'post':
            body = post('{}{}'.format(API_BASE, path), data=json.dumps(payload), headers=self._headers)
        elif method == 'get':
            body = get('{}{}'.format(API_BASE, path), headers=self._headers)
        elif method == 'patch':
            body = patch('{}{}'.format(API_BASE, path), data=json.dumps(payload), headers=self._headers)
        elif method == 'delete':
            body = delete('{}{}'.format(API_BASE, path), data=json.dumps(payload), headers=self._headers)
        elif method == 'put':
            body = put('{}{}'.format(API_BASE, path), data=json.dumps(payload), headers=self._headers)
        else:
            raise MalformedRequestError

        if body.status_code == '200' or body.status_code == '201':
            response_body = json.loads(body)
            return response_body

        if body.status_code == 400 or body.status_code == 400:
            raise MalformedRequestError(json.loads(body))
        elif body.status_code == 401 or body.status_code == 401:
            raise AuthenticationError(json.loads(body))
        elif body.status_code == 402 or body.status_code == 402:
            raise ProcessingError(json.loads(body))
        elif body.status_code == 404 or body.status_code == 404:
            raise ResourceNotFoundError(json.loads(body))
        elif body.status_code == 422 or body.status_code == 422:
            raise ParameterValidationError(json.loads(body))
        elif body.status_code == 500 or body.status_code == 500:
            raise ApiError(json.loads(body))
        else:
            raise FacturamaError(json.loads(body))

    def send_request(self):
        pass


class BuildRequest(Facturama):
    base_path = None

    @classmethod
    def create(cls, data):
        """

        :param data: dic with data for create object
        :return:
        """
        cls.build_http_request(cls, 'post', cls.base_path, data)

    def retrieve(self, oid):
        """

        :param oid: id of object retrieve
        :return:
        """
        self.build_http_request(self, 'get', '{}/{}'.format(self.base_path, oid))

    def all(self, id):
        """

        :param id: id of object retrieve
        :return:
        """
        self.build_http_request(self, 'get', self.base_path)

    def update(self, data, oid):
        """

        :param data: dic with data for create object
        :param oid: id of object
        :return:
        """
        self.build_http_request(self, 'put', '{}/{}'.format(self.base_path, oid), data)


class Customer(BuildRequest):
    """

    """
    base_path = 'Client'


class Product(BuildRequest):
    """

    """
    base_path = 'Product'


class Branch(BuildRequest):
    """

    """
    base_path = 'BranchOffice'
