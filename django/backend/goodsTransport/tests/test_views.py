from django.urls import reverse
from goodsTransport.tests.factories import PilotFactory, ShipFactory
from rest_framework import status
from rest_framework.test import APITestCase
from goodsTransport.models import Pilot, Ship, Contract, ResourceList
from goodsTransport.constants import FUEL_COST_PER_UNITY

class PilotViewSetTest(APITestCase):
  def setUp(self):
    self.pilot_1 = Pilot.objects.create(
      pilotCertification = '123',
      name = 'Wand',
      age = 20,
      credits = 20.25,
      locationPlanet = 'Calas'
    )
    self.pilot_2 = Pilot.objects.create(
      pilotCertification = '321',
      name = 'Wand2',
      age = 18,
      credits = 20.25,
      locationPlanet = 'Calas'
    )
    self.createPilot1 = {
      'pilotCertification': '111',
      'name': 'Wand3',
      'age': 18,
      'credits': 20.25,
      'locationPlanet': 'CALAS'
    }
    self.createPilot2 = {
      'pilotCertification': '222',
      'name': 'Wand4',
      'age': 17,
      'credits': 20.25,
      'locationPlanet': 'CALAS'
    }
    self.createPilot3 = {
      'pilotCertification': '222',
      'name': 'Wand4',
      'age': 17,
      'credits': -1,
      'locationPlanet': 'CALAS'
    }
    self.url_pilot_list = reverse('pilot-list')

  def test_get_pilot_list(self):
    pilotApi = self.client.get(
      self.url_pilot_list,
      format='json'
    )
    self.assertEqual(pilotApi.status_code, status.HTTP_200_OK)
    self.assertEqual(len(pilotApi.json()), 2)

  def test_create_pilot(self):
    pilotApi = self.client.post(
      self.url_pilot_list,
      self.createPilot1,
      format='json'
    )
    self.assertEqual(pilotApi.status_code, status.HTTP_201_CREATED)

  def test_create_pilot_under_18(self):
    pilotApi = self.client.post(
      self.url_pilot_list,
      self.createPilot2,
      format='json'
    )
    self.assertEqual(pilotApi.status_code, status.HTTP_400_BAD_REQUEST)

  def test_create_pilot_negative_credits(self):
    pilotApi = self.client.post(
      self.url_pilot_list,
      self.createPilot3,
      format='json'
    )
    self.assertEqual(pilotApi.status_code, status.HTTP_400_BAD_REQUEST)

class ShipViewSetTest(APITestCase):
  def setUp(self):
    self.ship_1 = ShipFactory()
    self.ship_2 = Ship.objects.create(
      fuelCapacity = 20,
      fuelLevel = 10,
      weightCapacity = 20,
    )
    self.createShipGood = {
      'fuelCapacity': 10,
      'fuelLevel': 9,
      'weightCapacity': 18
    }
    self.createShipNegativeFuelCapacity = {
      'fuelCapacity': -1,
      'fuelLevel': 10,
      'weightCapacity': 18
    }
    self.createShipNegativeFuelLevel = {
      'fuelCapacity': 10,
      'fuelLevel': -1,
      'weightCapacity': 18
    }
    self.createShipLevelGreaterCapacity = {
      'fuelCapacity': 10,
      'fuelLevel': 11,
      'weightCapacity': 20
    }
    self.url_ship_list = reverse('ship-list')
    self.pilot = PilotFactory(credits = 10)
    self.fuelGood = {
      'quantity': 1,
      'pilotCertification': self.pilot.pilotCertification
    }
    self.fuelLowCredits = {
      'quantity': int((self.pilot.credits/FUEL_COST_PER_UNITY)+10),
      'pilotCertification': self.pilot.pilotCertification
    }
    self.fuelMaxCapacity = {
      'quantity': self.ship_2.fuelCapacity + 5,
      'pilotCertification': self.pilot.pilotCertification
    }
    self.url_ship_fuel = reverse('ship-fuel', args=[self.ship_2.pk])

  def test_get_ship_list(self):
    shipApi = self.client.get(
      self.url_ship_list,
      format='json'
    )
    self.assertEqual(shipApi.status_code, status.HTTP_200_OK)
    self.assertEqual(len(shipApi.json()), 2)

  def test_create_ship(self):
    shipApi = self.client.post(
      self.url_ship_list,
      self.createShipGood,
      format='json'
    )
    self.assertEqual(shipApi.status_code, status.HTTP_201_CREATED)

  def test_create_ship_negative_fuelCapacity(self):
    shipApi = self.client.post(
      self.url_ship_list,
      self.createShipNegativeFuelCapacity,
      format='json'
    )
    self.assertEqual(shipApi.status_code, status.HTTP_400_BAD_REQUEST)

  def test_create_ship_negative_fuelLevel(self):
    shipApi = self.client.post(
      self.url_ship_list,
      self.createShipNegativeFuelLevel,
      format='json'
    )
    self.assertEqual(shipApi.status_code, status.HTTP_400_BAD_REQUEST)

  def test_create_ship_level_greater_capacity(self):
    shipApi = self.client.post(
      self.url_ship_list,
      self.createShipLevelGreaterCapacity,
      format='json'
    )
    self.assertEqual(shipApi.status_code, status.HTTP_400_BAD_REQUEST)

  def test_fuel_ship_good(self):
    shipApi = self.client.patch(
      self.url_ship_fuel,
      self.fuelGood,
      format='json'
    )
    self.assertEqual(shipApi.status_code, status.HTTP_202_ACCEPTED)

  def test_fuel_ship_low_credits(self):
    shipApi = self.client.patch(
      self.url_ship_fuel,
      self.fuelLowCredits,
      format='json'
    ) 
    self.assertEqual(shipApi.status_code, status.HTTP_400_BAD_REQUEST)

  def test_fuel_ship_max_fuel_capacity(self):
    shipApi = self.client.patch(
      self.url_ship_fuel,
      self.fuelMaxCapacity,
      format='json'
    ) 
    self.assertEqual(shipApi.status_code, status.HTTP_400_BAD_REQUEST)

class ContractViewSetTest(APITestCase):
  def setUp(self):
    self.resourceList = ResourceList.objects.create()
    self.contract = Contract.objects.create(
      description = '123',
      originPlanet = 'CALAS',
      destinationPlanet = 'CALAS',
      value = 20.25,
      payload = self.resourceList
    )
    self.contractOk = {
      'description': 'TestDescription',
      'originPlanet': 'CALAS',
      'destinationPlanet': 'CALAS',
      'value': 20.25,
      'payload': []
    }
    self.contractNegativeResourceWeight = {
      'description': 'TestDescription',
      'originPlanet': 'CALAS',
      'destinationPlanet': 'CALAS',
      'value': 20.25,
      'payload': [{'name':'WATER', 'weight': -20}]
    }
    self.url_contract_list = reverse('contract-list')

  def test_get_contract_list(self):
    contractApi = self.client.get(
      self.url_contract_list,
      format='json'
    )
    self.assertEqual(contractApi.status_code, status.HTTP_200_OK)
    self.assertEqual(len(contractApi.json()), 1)

  def test_create_contract(self):
    contractApi = self.client.post(
      self.url_contract_list,
      self.contractOk,
      format='json'
    )
    self.assertEqual(contractApi.status_code, status.HTTP_201_CREATED)

  def test_create_contractNegativeWeight(self):
    contractApi = self.client.post(
      self.url_contract_list,
      self.contractNegativeResourceWeight,
      format='json'
    )
    self.assertEqual(contractApi.status_code, status.HTTP_400_BAD_REQUEST)
