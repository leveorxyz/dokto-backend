import json
from unittest.mock import patch, Mock
from django.test import TestCase

from gateways.paypal import PaypalProvider

from .test_gateway import create_test_user


class PaypalTest(TestCase):

    def test_subscription(self):
        plan_id = 'P-1JB99519CN7739916MHFUXHA'
        user = create_test_user()
        res = PaypalProvider().init_subscription(user, 1, plan_id)
