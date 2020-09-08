from django.db import models
from django.contrib.auth.models import User


class Loan(models.Model):

    def __str__(self):
        return "Empréstimo %s" % (self.id)

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
        verbose_name='Taxa de Juros ao mês'
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

    acquittance_time = models.PositiveIntegerField(
        null=False,
        blank=False,
        default=1,
        verbose_name='Número de meses para quitação'
    )


    def get_balance_due(self):
        #DAYS_PER_MONTH = 30
        #DAYS_PER_YEAR = 360

        interest_rate_per_month = self.interest_rate / 100
        #ir_pro_rata = (interest_rate_per_month) #/ DAYS_PER_MONTH
        capital = self.nominal_value
        time = self.acquittance_time

        amount = capital * pow((1 + interest_rate_per_month), time)

        total_payment_balance = 0
        for payment in self.payment_set.all():
            total_payment_balance += payment.value
        
        return round(amount - total_payment_balance, 2)
    
    def check_payment(self, payment_value):
        current_balance_due = self.get_balance_due()

        return payment_value <= current_balance_due


class Payment(models.Model):

    def __str__(self):
        return "Pagamento %s de empréstimo %s" % (self.id, self.loan)

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
