from celery import shared_task
from .models import Payment
from datetime import datetime, timedelta
from ehr.models import PatientEncounters








@shared_task
def update_sign_date():
    #update release
    encounter = PatientEncounters.objects.filter(signed=True).filter(signed_date=None)
    id =encounter.appointment.id
    payment = Payment.objects.get(appointment=id)
    for signed in encounter:
        signed_date = datetime.date.today()
        expected_release_date = datetime.date.today() + timedelta(days = 14)
        payment.expected_release_date = expected_release_date
   


@shared_task
def update_doctor_wallet():
    # payment = Payment.objects.exclude(payment_date__gt=datetime.date.today())
    payment = Payment.objects.filter(payment_date__lte=datetime.date.today() ).filter(payment_released=False)
    #pay_to_wallet()

    return payment

@shared_task
def pay_to_wallet(payment):
    for value in payment:
        if value.payment_released == False:
            update_wallet()
            value.payment_released = True

def update_wallet():
    pass

    

