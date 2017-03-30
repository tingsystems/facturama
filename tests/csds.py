from . import BaseEndpointTestCase


class CSDSEndpointTestCase(BaseEndpointTestCase):
    def test_csds(self):
        self.client._credentials = ('pruebas', 'pruebas2011')
        self.client.api_lite = True
        self.client.csds.upload('RFC', 'csds.key', 'csds.cer', 'password')
        self.client.csds.get_by_rfc('RFC')
        csd = self.client.csds.delete('RFC')
        assert csd.status == True
