from django.urls import path
from financials import loan, payment


app_name = 'financials'


urlpatterns = [
    path('loans/new', loan.CreateLoan.as_view(), name='create_loan'),
    path('loans/list', loan.ListLoans.as_view(), name='list_loans'),
    path('loans/<int:pk>/detail', loan.DetailLoan.as_view(), name='detail_loan'),

    path('payment/create', payment.CreatePayment.as_view(), name='create_payment'),
    path('payments', payment.ListPayment.as_view(), name='list_payments'),
    path('payment/<int:pk>', payment.DetailPayment.as_view(), name='detail_payment'),
]