from django.test import TestCase
from goodsTransport.models import Pilot
from .factories import PilotFactory

class PilotTest(TestCase):
  def setUp(self):
    self.userAdult = PilotFactory()
    
  def test_newUser(self):
    self.assertIsInstance(self.userAdult, Pilot)
    self.assertTrue(Pilot.objects.all().count() == 1)