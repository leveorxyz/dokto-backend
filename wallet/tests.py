from django.test import TestCase

from user.models import User
from .models import Wallet


# Create your tests here.
class TestOnUserCreatedSignal(TestCase):
    def test_create_user(self):
        user = User.objects.create(email='test')
        wallet = Wallet.objects.filter(user=user).first()
        self.assertIsNotNone(wallet)
