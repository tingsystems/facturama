import unittest
import random
import facturama


class BaseEndpointTestCase(unittest.TestCase):
    random.seed()

    client = facturama
    customer_object = {
        "Id": "1111000",
        "Email": "test@test.com",
        "Address": {
            "Street": "Fenix One",
            "ExteriorNumber": "1",
            "InteriorNumber": "0",
            "Neighborhood": "Call me",
            "ZipCode": "59510",
            "Locality": "Xiquilpan",
            "Municipality": "Jiquilpan",
            "State": "MICHOACAN DE OCAMPO",
            "Country": "MX"
        },
        "Rfc": "GARR900630G98",
        "Name": "Pollitux"
    }
