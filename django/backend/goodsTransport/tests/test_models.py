from django.test import TestCase
from goodsTransport.models import *
from .factories import *

class PilotTest(TestCase):
  def setUp(self):
    self.pilot = PilotFactory()
    
  def test_newPilot(self):
    self.assertIsInstance(self.pilot, Pilot)
    self.assertTrue(Pilot.objects.all().count() == 1)

class ShipTest(TestCase):
  def setUp(self):
    self.ship = ShipFactory()
    
  def test_newShip(self):
    self.assertIsInstance(self.ship, Ship)
    self.assertTrue(Ship.objects.all().count() == 1)

class ResourceTest(TestCase):
  def setUp(self):
    contract = ContractFactory()
    self.resource = ResourceFactory(contract = contract)
    
  def test_newResource(self):
    self.assertIsInstance(self.resource, Resource)
    self.assertTrue(Resource.objects.all().count() == 1)

class ContractTest(TestCase):
  def setUp(self):
    self.contract = ContractFactory()
    
  def test_newContract(self):
    self.assertIsInstance(self.contract, Contract)
    self.assertTrue(Contract.objects.all().count() == 1)