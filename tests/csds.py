from . import BaseEndpointTestCase


class CSDSEndpointTestCase(BaseEndpointTestCase):
    def test_csds(self):
        self.client._credentials = ('test', 'test')
        self.client.api_lite = True
        self.client.sandbox = True
        self.client.csds.upload('rfc', 'csds.key', 'csds.cer', 'pass', v=2)
        csds = self.client.csds.get_by_rfc('LOGJ830412NM3', v=2)
        # csds = self.client.csds.delete('GUA140303IK8', v=2)
        assert csds.status
