from django.test import TestCase

from Client.forms import TransactionForm
from Client.models import ExtendedUser


class FormsTestCase(TestCase):
    def setUp(self):
        ExtendedUser.objects.create(username="TestUser1", password="pass", ITN=1234567890, balance=100)

    def test_transaction_form(self):
        user1 = ExtendedUser.objects.get(ITN=1234567890)

        data1 = {"users": user1, "numbers": user1.ITN, "summ": 100}
        data2 = {"users": user1, "numbers": user1.ITN, "summ": 0}

        form1 = TransactionForm(data=data1)
        form2 = TransactionForm(data=data2)

        self.assertTrue(form1.is_valid(), "check form with valid data")
        self.assertFalse(form2.is_valid(), "check form with wrong data")
