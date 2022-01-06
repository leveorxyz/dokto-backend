from unittest.mock import Mock, patch
from django.test import TestCase
from django.urls.base import reverse
from subscription.models import SubscriptionHistory, SubscriptionType
from subscription.views import SubscriptionBaseView

from user.models import ClinicInfo, DoctorInfo, PharmacyInfo, User
from .mixins import UserType


def create_test_user(user_type=UserType.DOCTOR):
    return User.objects.create(email="test@gmail.com", full_name='adewale bolu', user_type=user_type)

def create_test_doctor():
    return DoctorInfo.objects.create(user=create_test_user(UserType.DOCTOR), username='aa')

def create_test_clinic():
    return ClinicInfo.objects.create(user=create_test_user(UserType.CLINIC), username='aa')

def create_test_pharmacy():
    return PharmacyInfo.objects.create(user=create_test_user(UserType.PHARMACY), username='aa')

def create_test_subscription(user):
    return SubscriptionHistory.objects.create(user=user, payment_method='P', payment_ref='ref', active=True, amount=50)
    

class TestSubscriptionBaseView(TestCase):
    def test_get_object(self):
        doctor = create_test_doctor()
        view = SubscriptionBaseView(request=Mock(user=doctor.user))
        self.assertEqual(view.get_object(), doctor)

class TestSubscriptionView(TestCase):
    # def test_subscription_handle(self):
    #     doctor = create_test_doctor()
    #     request=Mock(user=doctor.user, data={'payment_method': 'O'})
    #     view = SubscriptionBaseView(request=request)
    #     view.create(request=request)

    @patch('gateways.gateway.Gateway.subscribe', return_value=("id", "url"))
    @patch('rest_framework.authentication.TokenAuthentication.authenticate')
    def test_subscription_api(self, mock_auth, _mock_subscribe):
        # test doctor on pay as you go plan(default)
        doctor = create_test_doctor()
        mock_auth.return_value = doctor.user, 'mm'
        data={'payment_method': 'P'}
        path = reverse('subscription:subscribe')
        res = self.client.post(path, data=data)
        self.assertEqual(res.status_code, 400)

        doctor.subscription_type = SubscriptionType.MEMBERSHIP
        doctor.save()
        res = self.client.post(path, data=data)
        self.assertEqual(res.status_code, 200)
        res_body = res.json()
        self.assertEqual(res_body['approval_url'], 'url')
        self.assertEqual(res_body['payment_method'], 'P')

class TestUnsubscribeView(TestCase):

    @patch('gateways.gateway.Gateway.cancel_subscription', return_value=None)
    @patch('rest_framework.authentication.TokenAuthentication.authenticate')
    def test_subscription_api(self, mock_auth, _mock_subscribe):
        # test doctor not on any subscription plan
        doctor = create_test_doctor()
        mock_auth.return_value = doctor.user, 'mm'
        path = reverse('subscription:unsubscribe')
        res = self.client.post(path)
        self.assertEqual(res.status_code, 400)

        # Test doctor on subscription plan
        doctor.subscription_type = SubscriptionType.MEMBERSHIP
        doctor.current_subscription = create_test_subscription(doctor.user)
        doctor.is_active = True
        doctor.save()
        res = self.client.post(path)
        self.assertEqual(res.status_code, 200)

class TestChangeSubscriptionView(TestCase):
    # @patch('gateways.gateway.Gateway.cancel_subscription', return_value=None)
    @patch('rest_framework.authentication.TokenAuthentication.authenticate')
    def test_subscription_api(self, mock_auth):
        # test doctor not on any subscription plan
        doctor = create_test_doctor()
        mock_auth.return_value = doctor.user, 'mm'
        path = reverse('subscription:unsubscribe')
        res = self.client.post(path)
        self.assertEqual(res.status_code, 400)

        # Test doctor on subscription plan
        doctor.subscription_type = SubscriptionType.MEMBERSHIP
        doctor.current_subscription = create_test_subscription(doctor.user)
        doctor.is_active = True
        doctor.save()
        res = self.client.post(path)
        self.assertEqual(res.status_code, 200)