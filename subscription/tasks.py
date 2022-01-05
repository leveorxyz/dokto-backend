from datetime import datetime, timedelta
from .models import SubscriptionHistory

# TODO: Move to celery beat with daily interval
def end_cancelled_subscriptions():
    latest_end_date = datetime.today() - timedelta(days=1)
    # Filter by subscriptions with end date less than today and is currently active
    histories = SubscriptionHistory.objects.filter(subscription_end__lt=latest_end_date).filter(active=True).filter(paused=False)
    for history in histories:
        history.set_paused()
