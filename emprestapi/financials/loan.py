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
    Endpoint for loan's creation,
    receives nominal_value, interest_rate, bank name, acquittance_time 
    and returns the created Loan the data is valid.
    ---------
    Accept the following POST parameters: 
        nominal_value,
        interest_rate,
        bank,
        acquittance_time
    Requires an authorization Token
    Return JSON with the loan's data.
    """

    class Meta:
        model = Loan
    
    permission_classes = [
        IsAuthenticated
    ]
    serializer_class = LoanSerializer

    def create(self, request, *args,**kwargs):
        client_ip = get_client_ip_address(request)
        user = request.user

        loan = LoanSerializer(data=request.data)
        if loan.is_valid():
            loan.save(ip_adress=client_ip, client=user)
            return Response(data=loan.data, status=status.HTTP_201_CREATED)

        return Response(data=loan.errors, status=status.HTTP_400_BAD_REQUEST)


class ListLoans(ListAPIView):
    """
    Endpoint for listing the client's loans.
    ---------
    Accepts a Token authenticated GET request
    Returns a JSON list with loans data.
    """

    permission_classes = [
        IsAuthenticated
    ]
    serializer_class = LoanSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Loan.objects.filter(client=user)

        return queryset


class DetailLoan(RetrieveAPIView):
    """
    Endpoint for retrieving a specific loan's data.
    ---------
    Accepts a Token authenticated GET request with the loan's id.
    Returns a JSON list with the loan's data.
    """
    permission_classes = [
        IsAuthenticated
    ]
    serializer_class = LoanSerializer

    def get(self, request, pk, format=None):
        user = request.user

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
        
