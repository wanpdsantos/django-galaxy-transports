from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from goodsTransport.models import Pilot, Ship

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
    self.ship_1 = Ship.objects.create(
      fuelCapacity = 25,
      fuelLevel = 12,
      weightCapacity = 15,
    )
    self.ship_2 = Ship.objects.create(
      fuelCapacity = 20,
      fuelLevel = 10,
      weightCapacity = 18,
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
    self.url_pilot_list = reverse('ship-list')

  def test_get_ship_list(self):
    shipApi = self.client.get(
      self.url_pilot_list,
      format='json'
    )
    self.assertEqual(shipApi.status_code, status.HTTP_200_OK)
    self.assertEqual(len(shipApi.json()), 2)

  def test_create_ship(self):
    shipApi = self.client.post(
      self.url_pilot_list,
      self.createShipGood,
      format='json'
    )
    self.assertEqual(shipApi.status_code, status.HTTP_201_CREATED)

  def test_create_ship_negative_fuelCapacity(self):
    shipApi = self.client.post(
      self.url_pilot_list,
      self.createShipNegativeFuelCapacity,
      format='json'
    )
    self.assertEqual(shipApi.status_code, status.HTTP_400_BAD_REQUEST)

  def test_create_pilot_negative_fuelLevel(self):
    shipApi = self.client.post(
      self.url_pilot_list,
      self.createShipNegativeFuelLevel,
      format='json'
    )
    self.assertEqual(shipApi.status_code, status.HTTP_400_BAD_REQUEST)

  def test_create_pilot_level_greater_capacity(self):
    shipApi = self.client.post(
      self.url_pilot_list,
      self.createShipLevelGreaterCapacity,
      format='json'
    )
    self.assertEqual(shipApi.status_code, status.HTTP_400_BAD_REQUEST)


