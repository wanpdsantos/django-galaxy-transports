from django.test import TestCase
from goodsTransport.models import *
from .factories import *

class PilotTest(TestCase):
  def setUp(self):
    self.userAdult = PilotFactory()
    
  def test_newPilot(self):
    self.assertIsInstance(self.userAdult, Pilot)
    self.assertTrue(Pilot.objects.all().count() == 1)

class ShipTest(TestCase):
  def setUp(self):
    self.ship = ShipFactory()
    
  def test_newShip(self):
    self.assertIsInstance(self.ship, Ship)
    self.assertTrue(Ship.objects.all().count() == 1)

class ResourceTest(TestCase):
  def setUp(self):
    self.resource = ResourceFactory()
    
  def test_newResource(self):
    self.assertIsInstance(self.resource, Resource)
    self.assertTrue(Resource.objects.all().count() == 1)