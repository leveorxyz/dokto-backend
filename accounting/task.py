from celery import shared_task
from .models import Payment
from datetime import datetime



@shared_task
def update_doctor_wallet():
    payment = Payment.objects.exclude(payment_date__gt=datetime.date.today())
    # update = [ pay_date, payment.released = True for pay_date in payment.payment_date if payment.released == False and payment.payment_date == datetime.date.today() ]
    for pay_date in payment.payment_date:
        if payment.released == False and payment.payment_date == datetime.date.today():
            payment.released = True
            #get doctor and move the money to doctor address
            # wallet_balance += payment.amount_paid


    

