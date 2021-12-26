from django.urls import path

from wallet.views import PaymentHistoryView, PayoutHistoryView, TransactionHistoryView, WalletDetailView

urlpatterns = [
    path('transactions', TransactionHistoryView.as_view({'get': 'list'}), name='transactions'),
    path('payments', PaymentHistoryView.as_view({'get': 'list'}), name='payments'),
    path('payouts', PayoutHistoryView.as_view({'get': 'list'}), name='payouts'),
    path('my-wallet', WalletDetailView.as_view({'get': 'retrieve'}), name='wallet'),
]