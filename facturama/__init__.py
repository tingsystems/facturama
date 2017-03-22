#!/usr/bin/python
# coding: utf-8
# (c) 2017 Raul Granados <@pollitux>

import base64
from requests import request

try:
    import json
except ImportError:
    import simplejson as json

__version__ = '0.0.3'
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
    Build request facturama API
    """

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
    def build_http_request(cls, method, path, payload=None, params=None):
        cls.aut_api()
        method = str(method).lower()
        body = request(
            method, '{}{}'.format(API_BASE, path), data=json.dumps(payload), params=params, headers=cls._headers
        )
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

    def to_object(self, response):
        for key, value in response.items():
            setattr(self, key, value)
        return self

    @classmethod
    def create(cls, data):
        """

        :param data: dict with data for create object
        :return: object with data from response
        """
        return cls.to_object(cls, cls.build_http_request('post', cls.__name__, data))

    @classmethod
    def retrieve(cls, oid, params=None):
        """

        :param oid: id of object retrieve
        :return: object with data from response
        """
        return cls.to_object(cls, cls.build_http_request('get', '{}/{}'.format(cls.__name__, oid), params=params))

    @classmethod
    def all(cls, params=None):
        """
        :return: list of objects from response facturama api
        """
        return cls.build_http_request('get', cls.__name__, params=params)

    @classmethod
    def query(cls, params=None):
        """
        :return: list of objects from response facturama api
        """
        return cls.build_http_request('get', cls.__name__, params=params)

    @classmethod
    def update(cls, data, oid):
        """

        :param data: dict with data for create object
        :param oid: id of object
        :return: object with data from response
        """
        return cls.to_object(cls, cls.build_http_request('put', '{}/{}'.format(cls.__name__, oid), data))

    @classmethod
    def delete(cls, oid):
        """
        :param oid: id of object
        :return: None
        """
        return cls.build_http_request('delete', '{}/{}'.format(cls.__name__, oid))


class Client(Facturama):
    """
    Opr with Clients of Facturama API
    """


class Product(Facturama):
    """
    Opr with Products of Facturama API
    """


class BranchOffice(Facturama):
    """
    Opr with Branch Offices of Facturama API
    """


class Cfdi(Facturama):
    """
    Opr with Cfdi of Facturama API
    """

    @classmethod
    def get_by_file(cls, f, t, oid):
        """
        :return: get cfdi file by format and type
        """
        return cls.build_http_request('get', '{}/{}/{}/{}'.format(cls.__name__, f, t, oid))

    @classmethod
    def send_by_email(cls, t, oid, email):
        """
        :return: send Cfdi by email
        """
        return cls.build_http_request('post', '{}?cfdiType={}&cfdiId={}&email={}'.format(cls.__name__, t, oid, email))
