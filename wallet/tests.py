from unittest import mock
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from user.models import User
from .models import PaymentStatus, Wallet, WalletIncomingPayment, WalletPayout


# Create your tests here.
class TestOnUserCreatedSignal(TestCase):
    def test_create_user(self):
        user = User.objects.create(email='test')
        wallet = Wallet.objects.filter(user=user).first()
        self.assertIsNotNone(wallet)


@mock.patch('core.classes.CustomTokenAuthentication.authenticate')
class ViewTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create(email="a@b.c", password='aaaaaaaaaa')
        self.wallet = Wallet.objects.get(user=self.user)
        WalletIncomingPayment.objects.create(wallet=self.wallet, amount=10000, amount_charged=10, status=PaymentStatus.SUCCESS)
        WalletIncomingPayment.objects.create(wallet=self.wallet, amount=1000, amount_charged=10, status=PaymentStatus.SUCCESS)
        WalletPayout.objects.create(wallet=self.wallet, amount=5000, status=PaymentStatus.SUCCESS)
        WalletPayout.objects.create(wallet=self.wallet, amount=500, status=PaymentStatus.SUCCESS)
    
    
    def test_transaction_history(self, authenticate_function):
        authenticate_function.return_value = self.user, None

        url = reverse('wallet:transactions')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        items = response.json()
        self.assertEqual(len(items), 4)
        
        # Confirm correct time arrangement
        item1 = items[0]
        self.assertEqual(item1.get('amount'), 500)

    def test_payout_history(self, authenticate_function):
        authenticate_function.return_value = self.user, None

        url = reverse('wallet:payouts')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        items = response.json()
        self.assertEqual(len(items), 2)

        # Confirm correct time arrangement
        item1 = items[0]
        self.assertEqual(item1.get('amount'), 500)

    def test_payment_history(self, authenticate_function):
        authenticate_function.return_value = self.user, None

        url = reverse('wallet:payments')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        items = response.json()
        self.assertEqual(len(items), 2)
        
        # Confirm correct time arrangement
        item1 = items[0]
        self.assertEqual(item1.get('amount'), 1000)

    def test_wallet(self, authenticate_function):
        authenticate_function.return_value = self.user, None

        url = reverse('wallet:wallet')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        obj = response.json()
        self.assertEqual(obj.get('id'), str(self.wallet.id))
