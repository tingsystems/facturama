from . import BaseEndpointTestCase


class CSDSEndpointTestCase(BaseEndpointTestCase):
    def test_csds(self):
        self.client._credentials = ('pruebas', 'pruebas2011')
        self.client.api_lite = True
        assert csd.status == True
