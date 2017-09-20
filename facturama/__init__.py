#!/usr/bin/python
# coding: utf-8
# (c) 2017 Raul Granados <@pollitux>

import base64
from requests import request

try:
    import json
except ImportError:
    import simplejson as json

__version__ = '2.0.1'
__author__ = 'Raul Granados'

api_lite = False
sandbox = False

_credentials = ('', '')


class FacturamaError(Exception):
    def __init__(self, error_json):
        super(FacturamaError, self).__init__(error_json)
        self.error_json = error_json


class MalformedRequestError(FacturamaError):
    pass


class AuthenticationError(FacturamaError):
    pass


class ProcessingError(FacturamaError):
    pass


class ResourceNotFoundError(FacturamaError):
    pass


class ParameterValidationError(FacturamaError):
    pass


class ApiError(FacturamaError):
    pass


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
    def build_http_request(cls, method, path, payload=None, params=None, version=0):
        """

        :param method: get, post, patch, put
        :param path: resource in the Facturama API
        :param payload: request body
        :param params: query params by url
        :param version: cfdi version 0 api, 1 api and cfdi 3.3, 2 api-lite, 3 api-lite and cfdi 3.3
        :return:
        """
        # urls base of facturama api
        uris = [
            'https://www.api.facturama.com.mx/api/',
            'https://www.api.facturama.com.mx/api/2/',
            'https://www.api.facturama.com.mx/api-lite/',
            'https://www.api.facturama.com.mx/2/api-lite/',
        ]
        api_base = uris[version]
        cls.aut_api()
        method = str(method).lower()

        body = request(
            method, '{}{}'.format(api_base, path), data=json.dumps(payload), params=params, headers=cls._headers
        )
        if body.status_code == 200 or body.status_code == 201 or body.status_code == 204:
            response_body = {'status': True}
            try:
                response_body = body.json()
            except Exception:
                pass
            return response_body

        if body.status_code == 400:
            raise MalformedRequestError(body.json())
        elif body.status_code == 401:
            raise AuthenticationError(body.json())
        elif body.status_code == 402:
            raise ProcessingError(body.json())
        elif body.status_code == 404:
            raise ResourceNotFoundError(body.json())
        elif body.status_code == 422:
            raise ParameterValidationError(body.json())
        elif body.status_code == 500:
            raise ApiError(body.json())
        else:
            raise FacturamaError(body.json())

    @classmethod
    def to_object(cls, response):
        for key, value in response.items():
            setattr(cls, key, value)
        return cls

    @classmethod
    def create(cls, data):
        """

        :param data: dict with data for create object
        :return: object with data from response
        """
        return cls.to_object(cls.build_http_request('post', cls.__name__, data))

    @classmethod
    def retrieve(cls, oid, params=None):
        """

        :params oid: id of object retrieve
        :return: object with data from response
        """
        return cls.to_object(cls.build_http_request('get', '{}/{}'.format(cls.__name__, oid), params=params))

    @classmethod
    def all(cls, params=None):
        """
        :type params: extra params for build request
        :return: list of objects from response facturama api
        """
        return cls.build_http_request('get', cls.__name__, params=params)

    @classmethod
    def query(cls, params=None):
        """
        :type params: extra params for build request
        :return: list of objects from response facturama api
        """
        return cls.build_http_request('get', cls.__name__, params=params)

    @classmethod
    def update(cls, data, oid):
        """
        :param oid: id object
        :type data: data
        :return: object with data from response
        """
        return cls.to_object(cls.build_http_request('put', '{}/{}'.format(cls.__name__, oid), data))

    @classmethod
    def delete(cls, oid):
        """
        :param oid: id object
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
    def create(cls, data, v=0):
        """

        :param v: cfdi version 0 api, 1 api and cfdi 3.3, 2 api-lite, 3 api-lite and cfdi 3.3
        :param data: dict with data for create object
        :return: object with data from response
        """
        return cls.to_object(cls.build_http_request('post', cls.__name__ if not api_lite else 'cfdis', data, version=v))

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

    @classmethod
    def delete(cls, oid):
        """
        :param oid: id object
        :return: None
        """
        v = 2 if api_lite else 0
        return cls.build_http_request(
            'delete', '{}/{}'.format(cls.__name__ if not api_lite else 'cfdis', oid), version=v
        )


class csds(Facturama):
    """
    Opr with csds of Facturama API
    """

    @classmethod
    def get_by_rfc(cls, rfc):
        """
        get csds by rfc
        :return: object with data from response
        """
        return cls.to_object(cls.build_http_request('get', '{}/{}'.format(cls.__name__, rfc)))

    @classmethod
    def create(cls, data):
        raise NotImplemented('Method not implemented')

    @classmethod
    def upload(cls, rfc, path_key, path_cer, password, encode=False):
        """

        :param encode:
        :param rfc:
        :param path_key:
        :param path_cer:
        :param password:
        :return: object with data from response
        """
        file_key, file_cer = path_key, path_cer
        if not encode:
            with open(path_key, 'rb') as f:
                file_key = base64.b64encode(f.read()).decode('utf-8')

            with open(path_cer, 'rb') as f:
                file_cer = base64.b64encode(f.read()).decode('utf-8')

        data = {
            'Rfc': str(rfc).upper(), 'Certificate': file_cer, 'PrivateKey': file_key, 'PrivateKeyPassword': password
        }
        return cls.build_http_request('post', cls.__name__, data)
