from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
from django.urls import reverse

from financials.models import Loan


class LoanTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            email='testuser@email.com', 
            password='123test'
        )

        token = Token.objects.create(user=self.user)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.loan = Loan.objects.create(
            nominal_value= 6000.00,
            interest_rate= 2.2,
            bank= "BRB",
            acquittance_time=3,
            client=self.user,
        )
        self.valid_loan_data = {
            "nominal_value": 6000.00,
            "interest_rate": 2.2,
            "bank": "BRB",
            "acquittance_time": 3
        }
        self.valid_loan_dict = {
            'nominal_value': '6000.00', 
            'interest_rate': '2.20', 
            'bank': 'BRB', 
            'client': 2, 
            'ip_adress': '', 
            'id': 3, 
            'acquittance_time': 3
        }
        self.invalid_loan_data = {}



    def test_create_loan(self):
        """
        Ensure we can create a new loan object.
        """
        
        response = self.client.post(reverse('financials:create_loan'), self.valid_loan_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Loan.objects.count(), 2)

    def test_loan_field_validation(self):
        """
        Should not save invalid loan.
        """
        NUMBER_OF_MANDATORY_FIELDS = 3

        response = self.client.post(reverse('financials:create_loan'), self.invalid_loan_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data), NUMBER_OF_MANDATORY_FIELDS)

    def test_list_loans(self):
        """
        Ensure it's possible to get a client's loans list.
        """
        
        response = self.client.get(reverse('financials:list_loans'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 1)

    def test_get_loan(self):
        """
        Ensure it's possible to get a client's specific loan.
        """
        loan_id = self.loan.id
        
        response = self.client.get('/financials/loans/%s/detail' % loan_id, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response.data.pop('balance_due')
        response.data.pop('solicitation_date')
        self.assertDictEqual(response.data, self.valid_loan_dict)

    def test_get_other_user_loan(self):
        """
        Ensure it's not possible to get loan data from another client.
        """

        new_user = User.objects.create_user(
            username='testuser2', 
            email='testuser2@email.com', 
            password='123test'
        )
        new_loan = Loan.objects.create(
            nominal_value= 500.00,
            interest_rate= 1.0,
            bank= "ITAU",
            acquittance_time=2,
            client=new_user,
        )

        response = self.client.get('/financials/loans/%s/detail' % new_loan.id, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_loan_balance_due(self):
        """
        Ensure a new loan object has the correct balance due.
        """
        BALANCE_DUE_6k_3MONTH = 6404.78

        response = self.client.post(reverse('financials:create_loan'), self.valid_loan_data, format='json')
        self.assertEqual(float(response.data.get('balance_due')), BALANCE_DUE_6k_3MONTH)