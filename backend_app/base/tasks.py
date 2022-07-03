import string

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from datetime import datetime, timedelta

from .models import BillingDetails

from celery import shared_task

@shared_task
def async_bill_generation(order):
    time = datetime.now()
    expected_arrival = order.expected_arrival
    delay_time = (time - expected_arrival).total_seconds()
    bill = BillingDetails(order, order_delay_time = delay_time/60)
    bill.save()
