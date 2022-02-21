from django.test import TestCase
from django.core.exceptions import ValidationError
from goodsTransport.validators import validate_age

class ValidatorsTest(TestCase):
  def setUp(self):
    self.ageAdult = 20
    self.ageTeen = 17
    
  def test_validate_age(self):
    self.assertTrue(validate_age(20) == None)
    with self.assertRaises(ValidationError):
      validate_age(self.ageTeen)

