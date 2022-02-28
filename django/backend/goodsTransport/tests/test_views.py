from django.urls import reverse
from goodsTransport.tests.factories import PilotFactory, \
ShipFactory, ContractFactory, ResourceListFactory, ResourceFactory
from rest_framework import status
from rest_framework.test import APITestCase
from goodsTransport.models import Ship, ResourceList, Pilot
from goodsTransport.constants import FUEL_COST_PER_UNITY, ROUTES

class PilotViewSetTest(APITestCase):
  def setUp(self):
    self.initialFuel = 50
    self.shipPilotAqua = ShipFactory(fuelLevel = self.initialFuel)
    self.shipPilotCalas = ShipFactory(fuelLevel = self.initialFuel)
    self.shipLowFuel = ShipFactory(fuelLevel = 1)
    self.shipLowCapacity = ShipFactory(fuelLevel = 100, weightCapacity=1)
    self.pilotAqua = PilotFactory(locationPlanet='AQUA', ship=self.shipPilotAqua)
    self.pilotCalas = PilotFactory(locationPlanet='CALAS', ship=self.shipPilotCalas)
    self.pilotCalasWithoutShip = PilotFactory(locationPlanet='CALAS', ship=None)
    self.pilotCalasShipLowFuel = PilotFactory(locationPlanet='CALAS', ship=self.shipLowFuel)
    self.pilotCalasShipLowWeightCapacity = PilotFactory(locationPlanet='CALAS', ship=self.shipLowCapacity)
    resourceList = ResourceListFactory()
    ResourceFactory(list=resourceList)
    self.contract = ContractFactory(status='OPEN', payload=resourceList)
    self.contractAlreadyAccepted = ContractFactory(status='ACCEPTED', payload=resourceList, pilot=self.pilotAqua)
    self.contractGreaterWeight = ContractFactory(
      status='OPEN', 
      payload=resourceList, 
      pilot=self.pilotCalasShipLowWeightCapacity
    )
    
    self.pilotAllGood = {
      'pilotCertification': '111',
      'name': 'Wand3',
      'age': 20,
      'credits': 20.25,
      'locationPlanet': 'CALAS'
    }
    self.pilotUnder18 = {
      'pilotCertification': '222',
      'name': 'Wand4',
      'age': 17,
      'credits': 20.25,
      'locationPlanet': 'CALAS'
    }
    self.pilotNegativeCredits = {
      'pilotCertification': '333',
      'name': 'Wand4',
      'age': 17,
      'credits': -1,
      'locationPlanet': 'CALAS'
    }
    self.url_pilot_list = reverse('pilot-list')
    self.url_pilot_contract = reverse('pilot-contracts', args=[self.pilotAqua.pk])
    self.url_pilot_contract_greaterWeight = reverse('pilot-contracts', args=[self.pilotCalasShipLowWeightCapacity.pk])
    self.url_pilot_travel_good_route = reverse('pilot-travels', args=[self.pilotCalas.pk]) + '?destination=Andvari'
    self.url_pilot_travel_blocked_route = reverse('pilot-travels', args=[self.pilotAqua.pk]) + '?destination=Andvari'
    self.url_pilot_travel_without_ship = reverse('pilot-travels', args=[self.pilotCalasWithoutShip.pk]) + '?destination=Andvari'
    self.url_pilot_travel_low_fuel = reverse('pilot-travels', args=[self.pilotCalasShipLowFuel.pk]) + '?destination=Andvari'

  def test_get_pilot_list(self):
    pilotApi = self.client.get(
      self.url_pilot_list,
      format='json'
    )
    self.assertEqual(pilotApi.status_code, status.HTTP_200_OK)
    self.assertEqual(len(pilotApi.json()), 5)

  def test_create_pilot(self):
    pilotApi = self.client.post(
      self.url_pilot_list,
      self.pilotAllGood,
      format='json'
    )
    self.assertEqual(pilotApi.status_code, status.HTTP_201_CREATED)

  def test_create_pilot_under_18(self):
    pilotApi = self.client.post(
      self.url_pilot_list,
      self.pilotUnder18,
      format='json'
    )
    self.assertEqual(pilotApi.status_code, status.HTTP_400_BAD_REQUEST)

  def test_create_pilot_negative_credits(self):
    pilotApi = self.client.post(
      self.url_pilot_list,
      self.pilotNegativeCredits,
      format='json'
    )
    self.assertEqual(pilotApi.status_code, status.HTTP_400_BAD_REQUEST)

  def test_pilot_accept_contract(self):
    pilotApi = self.client.post(
      self.url_pilot_contract,
      {'contract_id': self.contract.id},
      format='json'
    )
    self.assertEqual(pilotApi.status_code, status.HTTP_202_ACCEPTED)

  def test_pilot_accept_contract_greater_weight(self):
    pilotApi = self.client.post(
      self.url_pilot_contract_greaterWeight,
      {'contract_id': self.contractGreaterWeight.id},
      format='json'
    )
    self.assertEqual(pilotApi.status_code, status.HTTP_400_BAD_REQUEST)

  def test_pilot_accept_contract_already_accepted(self):
    pilotApi = self.client.post(
      self.url_pilot_contract,
      {'contract_id': self.contractAlreadyAccepted.id},
      format='json'
    )
    self.assertEqual(pilotApi.status_code, status.HTTP_400_BAD_REQUEST)

  def test_pilot_accept_contract_missing_contractId(self):
    pilotApi = self.client.post(
      self.url_pilot_contract,
      {},
      format='json'
    )
    self.assertEqual(pilotApi.status_code, status.HTTP_404_NOT_FOUND)

  def test_pilot_travel_between_planets(self):
    pilotApi = self.client.patch(
      self.url_pilot_travel_good_route,
      {},
      format='json'
    )
    ship = Ship.objects.get(pk=self.shipPilotCalas.pk)
    self.assertEqual(ship.fuelLevel, self.initialFuel - ROUTES['CALAS-ANDVARI']['fuelCost'])
    self.assertEqual(pilotApi.status_code, status.HTTP_202_ACCEPTED)

  def test_pilot_travel_between_planets_blocked_route(self):
    pilotApi = self.client.patch(
      self.url_pilot_travel_blocked_route,
      {},
      format='json'
    )
    self.assertEqual(pilotApi.status_code, status.HTTP_400_BAD_REQUEST)

  def test_pilot_travel_between_planets_without_ship(self):
    pilotApi = self.client.patch(
      self.url_pilot_travel_without_ship,
      {},
      format='json'
    )
    self.assertEqual(pilotApi.status_code, status.HTTP_400_BAD_REQUEST)

  def test_pilot_travel_between_planets_low_fuel(self):
    pilotApi = self.client.patch(
      self.url_pilot_travel_low_fuel,
      {},
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

  def test_create_ship_level_greater_than_capacity(self):
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
    resourceList = ResourceList.objects.create()
    self.ship = ShipFactory()
    self.initialCredits = 100
    self.pilot = PilotFactory(ship=self.ship, credits=self.initialCredits, locationPlanet= 'CALAS' )
    self.contractOpen = ContractFactory(payload=resourceList, status='OPEN')
    self.contractAccepted = ContractFactory(
      payload=resourceList, 
      status='ACCEPTED', 
      pilot=self.pilot,
      originPlanet = 'CALAS',
      destinationPlanet='AQUA'
    )
    self.contractAcceptedDifferentOrigin = ContractFactory(
      payload=resourceList, 
      status='ACCEPTED', 
      pilot=self.pilot,
      originPlanet = 'ANDVARI',
      destinationPlanet='AQUA'
    )
    self.contractAlreadyConcluded = ContractFactory(payload=resourceList, status='CONCLUDED', pilot=self.pilot)
    self.contractAllGood = {
      'description': 'TestDescription',
      'originPlanet': 'CALAS',
      'destinationPlanet': 'AQUA',
      'value': 20.25,
      'payload': []
    }
    self.contractSameOriginAndDestination= {
      'description': 'TestDescription',
      'originPlanet': 'CALAS',
      'destinationPlanet': 'CALAS',
      'value': 20.25,
      'payload': []
    }
    self.contractNegativeResourceWeight = {
      'description': 'TestDescription',
      'originPlanet': 'CALAS',
      'destinationPlanet': 'AQUA',
      'value': 20.25,
      'payload': [{'name':'WATER', 'weight': -20}]
    }
    self.url_contract_list = reverse('contract-list')
    self.url_contract_open_fullfill = reverse(
      'contract-fullfill', 
      args=[self.contractOpen.pk]
    )
    self.url_contract_concluded_fullfill = reverse(
      'contract-fullfill',
      args=[self.contractAlreadyConcluded.pk]
    )
    self.url_contract_accepted_fullfill = reverse(
      'contract-fullfill', 
      args=[self.contractAccepted.pk]
    )
    self.url_contract_accepted_not_at_start_planet = reverse(
      'contract-fullfill', 
      args=[self.contractAcceptedDifferentOrigin.pk]
    )

  def test_get_contract_list(self):
    contractApi = self.client.get(
      self.url_contract_list,
      format='json'
    )
    self.assertEqual(contractApi.status_code, status.HTTP_200_OK)
    self.assertEqual(len(contractApi.json()), 4)

  def test_create_contract(self):
    contractApi = self.client.post(
      self.url_contract_list,
      self.contractAllGood,
      format='json'
    )
    self.assertEqual(contractApi.status_code, status.HTTP_201_CREATED)

  def test_create_contract_SameOriginAndDestination(self):
    contractApi = self.client.post(
      self.url_contract_list,
      self.contractSameOriginAndDestination,
      format='json'
    )
    self.assertEqual(contractApi.status_code, status.HTTP_400_BAD_REQUEST)

  def test_create_contractNegativeWeight(self):
    contractApi = self.client.post(
      self.url_contract_list,
      self.contractNegativeResourceWeight,
      format='json'
    )
    self.assertEqual(contractApi.status_code, status.HTTP_400_BAD_REQUEST)

  def test_fullfill_contract(self):
    contractApi = self.client.patch(
      self.url_contract_accepted_fullfill,
      {},
      format='json'
    )
    pilotAfterFullfill = Pilot.objects.get(pk=self.pilot.pk)
    self.assertEqual(
      self.initialCredits+self.contractAccepted.value,
      pilotAfterFullfill.credits
    )
    self.assertEqual(contractApi.status_code, status.HTTP_202_ACCEPTED)

  def test_fullfill_contract_pilot_different_originPlanet(self):
    contractApi = self.client.patch(
      self.url_contract_accepted_not_at_start_planet,
      {},
      format='json'
    )
    self.assertEqual(contractApi.status_code, status.HTTP_400_BAD_REQUEST)

  def test_fullfill_contract_concluded(self):
    contractApi = self.client.patch(
      self.url_contract_concluded_fullfill,
      {},
      format='json'
    )
    self.assertEqual(contractApi.status_code, status.HTTP_400_BAD_REQUEST)

  def test_fullfill_contract_open(self):
    contractApi = self.client.patch(
      self.url_contract_open_fullfill,
      {},
      format='json'
    )
    self.assertEqual(contractApi.status_code, status.HTTP_400_BAD_REQUEST)

class ReportTotalWeightViewTest(APITestCase):
  def setUp(self):
    self.url = reverse('ReportTotalWeightByPlanet')
  
  def test_report_total_weight_by_planet(self):
    reportApi = self.client.get(
      self.url,
      format='json'
    )
    self.assertEqual(reportApi.status_code, status.HTTP_200_OK)
  
class ReportPilotResourcesTrasportedViewTest(APITestCase):
  def setUp(self):
    self.url = reverse('PilotResourceTransported')
  
  def test_report_pilot_resources_transported(self):
    reportApi = self.client.get(
      self.url,
      format='json'
    )
    self.assertEqual(reportApi.status_code, status.HTTP_200_OK)