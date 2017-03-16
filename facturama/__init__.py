#!/usr/bin/python
# coding: utf-8
# (c) 2017 Raul Granados <@pollitux>

import base64
from requests import post, get, patch, put, delete

try:
    import json
except ImportError:
    import simplejson as json

__version__ = '0.0.1'
__author__ = 'Raul Granados'

API_BASE = 'https://www.api.facturama.com.mx/api/'

_credentials = ('', '')


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
    """

    """

    base_path = None
    _headers = None

    @classmethod
    def aut_api(cls):
        _username, _password = _credentials
        cls._headers = {
            'Authorization': 'Basic %s' % (base64.b64encode(
                ('{}:{}'.format(_username, _password)).encode('utf-8'))).decode('ascii'),
            'content-type': 'application/json'
        }

    @classmethod
    def build_http_request(cls, method, path, payload=None):
        cls.aut_api()
        method = str(method).lower()
        if method == 'post':
            body = post('{}{}'.format(API_BASE, path), data=json.dumps(payload), headers=cls._headers)
        elif method == 'get':
            body = get('{}{}'.format(API_BASE, path), headers=cls._headers)
        elif method == 'patch':
            body = patch('{}{}'.format(API_BASE, path), data=json.dumps(payload), headers=cls._headers)
        elif method == 'delete':
            body = delete('{}{}'.format(API_BASE, path), data=json.dumps(payload), headers=cls._headers)
        elif method == 'put':
            body = put('{}{}'.format(API_BASE, path), data=json.dumps(payload), headers=cls._headers)
        else:
            raise MalformedRequestError

        if body.status_code == 200 or body.status_code == 201:
            response_body = body.json()
            return response_body

        if body.status_code == 400 or body.status_code == 400:
            raise MalformedRequestError(body.json())
        elif body.status_code == 401 or body.status_code == 401:
            raise AuthenticationError(body.json())
        elif body.status_code == 402 or body.status_code == 402:
            raise ProcessingError(body.json())
        elif body.status_code == 404 or body.status_code == 404:
            raise ResourceNotFoundError(body.json())
        elif body.status_code == 422 or body.status_code == 422:
            raise ParameterValidationError(body.json())
        elif body.status_code == 500 or body.status_code == 500:
            raise ApiError(body.json())
        else:
            raise FacturamaError(body.json())

    @classmethod
    def create(cls, data):
        """

        :param data: dic with data for create object
        :return:
        """
        return cls.build_http_request('post', cls.base_path, data)

    @classmethod
    def retrieve(cls, oid):
        """

        :param oid: id of object retrieve
        :return:
        """
        return cls.build_http_request('get', '{}/{}'.format(cls.base_path, oid))

    @classmethod
    def all(cls):
        """

        :param id: id of object retrieve
        :return:
        """
        return cls.build_http_request('get', cls.base_path)

    @classmethod
    def update(cls, data, oid):
        """

        :param data: dic with data for create object
        :param oid: id of object
        :return:
        """
        return cls.build_http_request('put', '{}/{}'.format(cls.base_path, oid), data)


class Customer(Facturama):
    """
    Opr with Clients of Facturama API
    """
    base_path = 'Client'


class Product(Facturama):
    """
    Opr with Products of Facturama API
    """
    base_path = 'Product'


class Branch(Facturama):
    """
    Opr with Branch Offices of Facturama API
    """
    base_path = 'BranchOffice'
