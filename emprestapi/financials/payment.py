from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from financials.models import Payment, Loan
from financials.serializers import PaymentSerializer
from financials.utils import get_client_ip_address


class CreatePayment(CreateAPIView):
    """
    Endpoint for loan's payment creation,
    receives a value and returns the Payment data if the payment is valid.
    ---------
    Accept the following POST parameters: payment's value, loan id
    Requires an authorization token
    Return JSON with payment's data.
    """

    model = Payment
    permission_classes = [
        IsAuthenticated
    ]
    serializer_class = PaymentSerializer

    def create(self, request, *args,**kwargs):
        user = request.user
        payment = PaymentSerializer(data=request.data)

        if payment.is_valid():
            loan = payment.validated_data.get('loan')
            valid_client = self.valid_client(loan, user)
            valid_payment_loan = self.valid_payment_loan(loan, payment.validated_data.get('value'))

            if valid_client and valid_payment_loan:
                payment.save()
                return Response(data=payment.data, status=status.HTTP_201_CREATED)
            elif not valid_client:
                data = {'Erro': 'O usuário não tem autorização para os dados deste empréstimo'}
                return Response(status=status.HTTP_403_FORBIDDEN)
            elif not valid_payment_loan:
                data = {'Erro': 'O valor do pagamento deve ser menor ou igual ao saldo devedor'}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
                

        return Response(data=payment.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def valid_client(self, loan, client):
        return client == loan.client
    
    def valid_payment_loan(self, loan, payment):
        return loan.check_payment(payment)


class ListPayment(ListAPIView):
    """
    Endpoint for listing the client's payment.
    ---------
    Accepts a Token authenticated GET request
    Returns a JSON list with payments data.
    """

    serializer_class = PaymentSerializer
    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):
        user = self.request.user
        queryset = Payment.objects.filter(loan__client=user)

        return queryset


class DetailPayment(RetrieveAPIView):
    """
    Endpoint for retrieving a specific payment's data.
    ---------
    Accepts a Token authenticated GET request with the payment's id.
    Returns a JSON list with the payment's data.
    """

    serializer_class = PaymentSerializer
    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request, pk, format=None):
        user = request.user

        try:
            payment = Payment.objects.get(pk=pk)
        except Payment.DoesNotExist:
            data = {'Erro': 'Não foi possível encontrar o pagamento solicitado'}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        if not self.valid_client(user, payment):
            data = {'Erro': 'Você não possui autorização para visualizar este pagamento'}
            return Response(data=data, status=status.HTTP_403_FORBIDDEN)

        serializer = PaymentSerializer(payment)

        return Response(serializer.data)
    
    def valid_client(self, client, payment):
        return client == payment.loan.client
        