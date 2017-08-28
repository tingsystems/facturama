from . import BaseEndpointTestCase


class CfdiEndpointTestCase(BaseEndpointTestCase):

    def test_cfdi_create(self):
        self.client._credentials = ('pruebas', 'pruebas2011')
        self.client.api_lite = True
        cfdi = self.client.Cfdi.delete('facturamaId')
        print(cfdi, 'sfdfdf')
        assert cfdi
