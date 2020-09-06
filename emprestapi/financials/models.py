from django.db import models
from django.contrib.auth.models import User


class Loan(models.Model):

    nominal_value = models.DecimalField(
        null=False, 
        blank=False,
        max_digits=12, 
        decimal_places=2,
        verbose_name='Valor emprestado pelo banco'
    )

    interest_rate = models.DecimalField(
        null=False, 
        blank=False,
        max_digits=5, 
        decimal_places=2,
        verbose_name='Taxa de Juros'
    )

    ip_adress = models.CharField(
        null=False, 
        blank=False, 
        help_text='Endereço de IP', 
        max_length=16
    )

    solicitation_date = models.DateTimeField(
        auto_now_add=True, 
        blank=False, 
        null=False,
        verbose_name='Data de solicitação'
    )

    bank = models.CharField(
        max_length=50,
        verbose_name='Banco fonte do empréstimo',
        null=False,
        blank=False
    )

    client = models.ForeignKey(
        User, 
        verbose_name='Cliente do empréstimo', 
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    def get_balance_due(self):
        total_payment_balance = 0
        for payment in self.payment_set.all():
            total_payment_balance += payment.value
        
        return self.nominal_value - total_payment_balance
    
    def check_payment(self, payment_value):
        current_balance_due = self.get_balance_due()

        return payment_value <= current_balance_due


class Payment(models.Model):

    loan = models.ForeignKey(
        Loan, 
        verbose_name='Empréstimo', 
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    solicitation_date = models.DateTimeField(
        auto_now_add=True, 
        blank=False, 
        null=False,
        verbose_name='Data de pagamento'
    )

    value = models.DecimalField(
        null=False, 
        blank=False,
        max_digits=12, 
        decimal_places=2,
        verbose_name='Valor do pagamento'
    )
