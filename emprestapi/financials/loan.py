from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from financials.models import Loan
from financials.serializers import LoanSerializer

from financials.utils import get_client_ip_address


class CreateLoan(CreateAPIView):
    """
    TODO
    """
    model = Loan
    permission_classes = [
        AllowAny
    ]
    serializer_class = LoanSerializer

    def create(self, request, *args,**kwargs):
        client_ip = get_client_ip_address(request)
        user = User.objects.all().last()

        loan = LoanSerializer(data=request.data)
        if loan.is_valid():
            loan.save(ip_adress=client_ip, client=user)
            return Response(data=loan.data, status=status.HTTP_201_CREATED)

        return Response(data=loan.errors, status=status.HTTP_400_BAD_REQUEST)


class ListLoans(ListAPIView):
    """
    TODO
    """

    serializer_class = LoanSerializer
    permission_classes = [
        AllowAny
    ]

    def get_queryset(self):
        user = User.objects.all().last()
        queryset = Loan.objects.filter(client=user)

        return queryset


class DetailLoan(RetrieveAPIView):
    """
    TODO
    """

    serializer_class = LoanSerializer
    permission_classes = [
        AllowAny
    ]

    def get(self, request, pk, format=None):
        user = User.objects.all().last()

        try:
            loan = Loan.objects.get(pk=pk)
        except Loan.DoesNotExist:
            data = {'Erro': 'Não foi possível encontrar o empréstimo solicitado'}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        if not self.valid_client(user, loan):
            data = {'Erro': 'Você não possui autorização para visualizar este empréstimo'}
            return Response(data=data, status=status.HTTP_403_FORBIDDEN)

        serializer = LoanSerializer(loan)

        return Response(serializer.data)
    
    def valid_client(self, client, loan):
        return client == loan.client
        
