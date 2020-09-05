from django.urls import path
from financials import views


app_name = 'financials'


urlpatterns = [
    path('list_loans/', views.ListLoans.as_view(), name='list_loans'),
]