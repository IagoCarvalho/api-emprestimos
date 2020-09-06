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
    TODO
    """
    model = Payment
    permission_classes = [
        AllowAny
    ]
    serializer_class = PaymentSerializer

    def create(self, request, *args,**kwargs):
        user = User.objects.all().last()
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
    TODO
    """

    serializer_class = PaymentSerializer
    permission_classes = [
        AllowAny
    ]

    def get_queryset(self):
        user = User.objects.all().last()
        queryset = Payment.objects.filter(loan__client=user)

        return queryset


class DetailPayment(RetrieveAPIView):
    """
    TODO
    """

    serializer_class = PaymentSerializer
    permission_classes = [
        AllowAny
    ]

    def get(self, request, pk, format=None):
        user = User.objects.all().last()

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
        