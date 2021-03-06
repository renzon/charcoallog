from django.test import TestCase

from charcoallog.bank.models import Extract
from charcoallog.investments.models import Investment, InvestmentDetails


class InvestmentModelTest(TestCase):
    """ M3A03 - WTTD """
    def setUp(self):
        data = dict(
            user_name='teste',
            date='2018-03-27',
            tx_op=00.00,
            money=94.42,
            kind='Títulos Públicos',
            which_target='Tesouro Direto',
            brokerage='Ativa'
        )
        Investment.objects.create(**data)

    def test_investments_exists(self):
        """ Test if investment is created"""
        self.assertTrue(Investment.objects.exists())

    def test_investment_details_exists(self):
        """ Test if details is created """
        self.assertTrue(InvestmentDetails.objects.exists())

    def test_update_investment_details(self):
        """ Test if created details object can be updated """
        obj = InvestmentDetails.objects.get()
        obj.segment = 'Selic 2023'
        obj.tx_or_price = 0.01
        obj.quant = 1.00
        obj.save(update_fields=['segment', 'tx_or_price', 'quant'])

        self.assertTrue(InvestmentDetails.objects.filter(segment='Selic 2023').exists())


class DataFromBankTest(TestCase):
    def setUp(self):
        self.user = 'teste'
        self.data = dict(
            user_name='you',
            date='2018-04-20',
            money=10.00,
            description='Ativa',
            category='investments',
            payment='principal',
        )
        Extract.objects.create(**self.data)

    def test_data_in_investments(self):
        data = Investment.objects.filter(brokerage='Ativa').exists()
        self.assertTrue(data)

    def test_data_not_in_investmentdetails(self):
        data = InvestmentDetails.objects.filter(kind='---').exists()
        self.assertFalse(data)
