from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from financials.models import Payment
from financials.serializers import LoanSerializer

from financials.utils import get_client_ip_address


class CreatePayment(CreateAPIView):
    model = Payment
    permission_classes = [
        AllowAny
    ]
    serializer_class = LoanSerializer

    def create(self, request, *args,**kwargs):
        user = User.objects.all().last()

        try:
            loan = loan.objects.get()
        if loan.is_valid():
            loan.save(ip_adress=client_ip, client=user)
            return Response(status=status.HTTP_201_CREATED)

        return Response(data=es.errors, status=status.HTTP_400_BAD_REQUEST)