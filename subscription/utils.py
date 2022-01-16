from subscription.mixins import UserType
from user.models import ClinicInfo, DoctorInfo, PharmacyInfo, User


def get_subscription_user(user: User):
    if user.user_type == UserType.CLINIC:
        return ClinicInfo.objects.get(user=user)
    if user.user_type == UserType.DOCTOR:
        return DoctorInfo.objects.get(user=user)
    if user.user_type == UserType.PHARMACY:
        return PharmacyInfo.objects.get(user=user)
    raise Exception()
