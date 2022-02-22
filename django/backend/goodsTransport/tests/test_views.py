from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from goodsTransport.models import Pilot

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

  def test_get_pilot(self):
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

