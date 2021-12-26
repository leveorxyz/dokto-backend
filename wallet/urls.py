from django.urls import path

from wallet.views import PaymentHistoryView, PayoutHistoryView, TransactionHistoryView

urlpatterns = [
    path('transactions', TransactionHistoryView.as_view({'get': 'list'}), name='transactions'),
    path('payments', PaymentHistoryView.as_view({'get': 'list'}), name='payments'),
    path('payouts', PayoutHistoryView.as_view({'get': 'list'}), name='payouts'),
]