from django.urls import path, include
from rest_framework import routers
from usermanagement import views


app_name = 'usermanagement'


urlpatterns = [
    path('list/', views.UserList.as_view(), name='list'),
    path('create/', views.CreateUser.as_view(), name='create')
]
