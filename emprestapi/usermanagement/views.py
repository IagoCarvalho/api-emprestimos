from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework import generics
from usermanagement.serializers import UserSerializer


class CreateUser(CreateAPIView):

    model = User
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer


    # def get_client_ip_address(request):
    #     http_x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        
    #     if http_x_forwarded_for:
    #         ip_address = http_x_forwarded_for.split(',')[-1].strip()
    #     else:
    #         ip_address = request.META.get('REMOTE_ADDR')
    #     return ip_addddress


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer