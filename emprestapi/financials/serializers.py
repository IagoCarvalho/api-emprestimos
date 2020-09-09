from rest_framework import serializers
from financials.models import Loan, Payment
from django.contrib.auth.models import User


class LoanSerializer(serializers.ModelSerializer):
    balance_due = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = [
            'nominal_value', 
            'interest_rate', 
            'solicitation_date', 
            'bank', 
            'client', 
            'ip_adress', 
            'id',
            'balance_due',
            'acquittance_time'
        ]
        extra_kwargs = {
            'client': {
                'read_only': True,
            },
            'ip_adress': {
                'read_only': True,
            },
            'id': {
                'read_only': True,
            },
            'balance_due': {
                'read_only': True
            }
        }
    
    def get_balance_due(self, loan):
        return loan.get_balance_due()


class PaymentSerializer(serializers.ModelSerializer):
    loan = serializers.SlugRelatedField(queryset=Loan.objects.all(), slug_field='id')

    class Meta:
        model = Payment
        fields = [
            'value', 
            'solicitation_date', 
            'loan',
            'id'
        ]
        extra_kwargs = {
            'solicitation_date': {
                'read_only': True,
            },
            'id': {
                'read_only': True,
            },
        }
