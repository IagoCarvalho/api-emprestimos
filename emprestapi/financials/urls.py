from django.urls import path
from financials import loan


app_name = 'financials'


urlpatterns = [
    path('loans/create', loan.CreateLoan.as_view(), name='create_loan'),
    path('loans/list', loan.ListLoans.as_view(), name='list_loans'),
    path('loans/<int:pk>/detail', loan.DetailLoan.as_view(), name='detail_loan'),
]