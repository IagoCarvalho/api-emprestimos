from django.urls import path, include

from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from usermanagement import views


app_name = 'usermanagement'


urlpatterns = [
    path('list/', views.UserList.as_view(), name='list'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('rest_auth/', include('rest_auth.urls')),
    path('rest_auth/registration/', include('rest_auth.registration.urls')),
]