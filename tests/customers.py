from . import BaseEndpointTestCase


class CustomerEndpointTestCase(BaseEndpointTestCase):
    def test_customer_create(self):
        self.client._credentials = ('pruebas', 'pruebas2011')

        customer = self.client.Customer.create(self.customer_object.copy())

        assert customer['Name'] == 'Pollitux'
        assert customer['Email'] == 'test@test.com'
        assert customer['Rfc'] == 'GARR900630G98'

    def test_customer_get(self):
        self.client._credentials = ('pruebas', 'pruebas2011')
        customer = self.client.Customer.all()
        assert customer
