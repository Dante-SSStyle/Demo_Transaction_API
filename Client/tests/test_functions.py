from django.core.exceptions import ValidationError
from django.test import TestCase

from Client.validators import validate_itn


class ValidatorsTestCase(TestCase):

    def test_validator(self):
        itn1 = "0123456789"
        itn2 = "123456789120"
        itn3 = "000123"
        itn4 = "000123abc000"

        self.assertEqual(validate_itn(itn1), itn1)
        self.assertEqual(validate_itn(itn2), itn2)
        self.assertRaises(ValidationError, validate_itn, itn3)
        self.assertRaises(ValidationError, validate_itn, itn4)
