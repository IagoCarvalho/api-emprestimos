from rest_framework import serializers
from financials.models import Loan, Payment


class LoanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Loan
        fields = ['nominal_value', 'interest_rate', 'solicitation_date', 'bank', 'client', 'ip_adress', 'id']
        extra_kwargs = {
            'client': {
                'read_only': True,
            },
            'ip_adress': {
                'read_only': True,
            },
            'id': {
                'read_only': True,
            }
        }

