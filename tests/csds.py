from . import BaseEndpointTestCase


class CSDSEndpointTestCase(BaseEndpointTestCase):
    def test_csds(self):
        self.client._credentials = ('user', 'pass')
        self.client.api_lite = True
        self.client.sandbox = False
        # self.client.csds.delete('rfc')
        self.client.csds.upload('rfc', 'csds.key', 'csds.cer', 'pass', v=2)
        csds = self.client.csds.get_by_rfc('rfc', v=2)
        assert csds.status
