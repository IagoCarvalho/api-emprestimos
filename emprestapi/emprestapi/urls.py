from django.contrib import admin
from django.urls import path, include
from financials import loan


urlpatterns = [
    path('', loan.ListLoans.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('users/', include('usermanagement.urls')),
    path('financials/', include('financials.urls', namespace='financials')),
    path('', include('django.contrib.auth.urls')),
]
