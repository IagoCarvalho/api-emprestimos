from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework import generics

from usermanagement.serializers import UserSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer