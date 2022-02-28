from django.urls import reverse
from django.shortcuts import get_object_or_404
from goodsTransport.serializers import PilotSerializer, ShipSerializer, \
  ContractSerializer, ResourceSerializer, ResourceListSerializer
from goodsTransport.models import Pilot, Ship, Contract, ResourceList, Resource
from goodsTransport.constants import FUEL_COST_PER_UNITY, ROUTES, PLANETS, RESOURCES
from goodsTransport.functions import totalWeightReportReducer
from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from functools import reduce
import json

class PilotViewSet(viewsets.ModelViewSet):
  queryset = Pilot.objects.all()
  serializer_class = PilotSerializer
  
  def pilot_travel_between_planets(self, *args, **kwargs):
    pilot = self.get_object()
    origin = pilot.locationPlanet
    destination = self.request.query_params.get('destination', '').upper()
    serializer = PilotSerializer(
      pilot, 
      data={'locationPlanet': destination},
      partial=True,
      context={'request': self.request}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()

    ship = pilot.ship
    serializerShip = ShipSerializer(
      ship,
      data={'fuelLevel': ship.fuelLevel - ROUTES[f"{origin}-{destination}"]['fuelCost']},
      partial=True,
      context={'request': self.request}
    )
    serializerShip.is_valid(raise_exception=True)
    serializerShip.save()
    return serializer.data

  @action(detail = True, methods = ['PATCH'])
  def travels(self, request, *args, **kwargs):
    requestType = {
      'PATCH': {
        'function': self.pilot_travel_between_planets,
        'statusCode': status.HTTP_202_ACCEPTED,
      }
    }
    return Response(
      requestType[request.method]['function'](), 
      status = requestType[request.method]['statusCode']
    )

  def get_pilot_ship(self):
    queryset = Ship.objects.filter(pilot=self.get_object())
    serializer = ShipSerializer(queryset, many=True,context={'request': self.request})
    return serializer.data

  def attach_ship_to_pilot(self):
    queryset = Ship.objects.all()
    ship = get_object_or_404(queryset, id = self.request.data.get('ship_id'))
    serializer = self.serializer_class(
      self.get_object(), 
      data={'ship':reverse("ship-detail", args=[ship.id])}, 
      partial=True,
      context={'request': self.request}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer.data

  def remove_ship_from_pilot(self):
    serializer = self.serializer_class(
      self.get_object(), 
      data={'ship': None}, 
      partial=True,
      context={'request': self.request}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer.data

  @action(detail = True, methods = ['GET', 'PATCH', 'DELETE'])
  def ships(self, request, *args, **kwargs):
    requestType = {
      'PATCH': {
        'function': self.attach_ship_to_pilot,
        'statusCode': status.HTTP_202_ACCEPTED,
      },
      'GET': {
        'function': self.get_pilot_ship,
        'statusCode': status.HTTP_200_OK,
      },
      'DELETE': {
        'function': self.remove_ship_from_pilot,
        'statusCode': status.HTTP_202_ACCEPTED,
      }
    }
    return Response(
      requestType[request.method]['function'](), 
      status = requestType[request.method]['statusCode']
    )

  def get_pilot_contracts(self):
    queryset = Contract.objects.filter(pilot=self.get_object())
    serializer = ContractSerializer(queryset, many=True,context={'request': self.request})
    return serializer.data

  def pilot_accept_contract(self):
    queryset = Contract.objects.all()
    contract = get_object_or_404(queryset, id = self.request.data.get('contract_id'))
    serializer = ContractSerializer(
      contract, 
      data={'status': 'ACCEPTED' , 'pilot': reverse("pilot-detail", args=[self.get_object().id]) }, 
      partial=True,
      context={'request': self.request}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer.data

  @action(detail = True, methods = ['GET','POST'])
  def contracts(self, request, *args, **kwargs):
    requestType = {
      'POST': {
        'function': self.pilot_accept_contract,
        'statusCode': status.HTTP_202_ACCEPTED,
      },
      'GET': {
        'function': self.get_pilot_contracts,
        'statusCode': status.HTTP_200_OK,
      }
    }
    return Response(
      requestType[request.method]['function'](), 
      status = requestType[request.method]['statusCode']
    )

class ShipViewSet(viewsets.ModelViewSet):
  queryset = Ship.objects.all()
  serializer_class = ShipSerializer

  @action(detail = True, methods = ['patch'])
  def fuel(self, request, *args, **kwargs):
    queryset = Pilot.objects.all()
    pilot = get_object_or_404(queryset, pilotCertification = request.data.get('pilotCertification'))
    serializer = PilotSerializer(
      pilot, 
      data={'credits': pilot.credits-request.data.get('quantity')*FUEL_COST_PER_UNITY}, 
      partial=True,
      context={'request': request}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    try:
      ship = self.get_object()
      serializer = ShipSerializer(
        ship, 
        data={
          'fuelLevel': ship.fuelLevel+request.data.get('quantity'),
          'fuelCapacity': ship.fuelCapacity
        }, 
        partial=True,
        context={'request': request}
      )
      serializer.is_valid(raise_exception=True)
      serializer.save()
    except serializers.ValidationError:
      serializerRollBack = PilotSerializer(
        pilot, 
        data={'credits': pilot.credits+request.data.get('quantity')*FUEL_COST_PER_UNITY}, 
        partial=True,
        context={'request': request}
      )
      serializerRollBack.is_valid(raise_exception=True)
      serializerRollBack.save()
      return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data, status = status.HTTP_202_ACCEPTED)

class ResourceListViewSet(viewsets.ModelViewSet):
  queryset = ResourceList.objects.all()
  serializer_class = ResourceListSerializer

class ResourceViewSet(viewsets.ModelViewSet):
  queryset = Resource.objects.all()
  serializer_class = ResourceSerializer

class ContractViewSet(viewsets.ModelViewSet):
  queryset = Contract.objects.all()
  serializer_class = ContractSerializer

  def create(self, request, *args, **kwargs):
    newResourceList = ResourceList.objects.create()
    items = list(map(
      lambda item: {
        'list': reverse("resourcelist-detail", args=[newResourceList.id]), 
        'name': item['name'], 
        'weight': item['weight']
      }, 
      request.data.get('payload')
    ))
    serializer = ResourceSerializer(data=items, many=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    contract = {
      'description': request.data.get('description'),
      'originPlanet': request.data.get('originPlanet'),
      'destinationPlanet':request.data.get('destinationPlanet'),
      'value': request.data.get('value'),
      'payload': reverse("resourcelist-detail", args=[newResourceList.id]),
      'status': 'OPEN'
    }
    serializer = ContractSerializer(data=contract, context={'request': request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status = status.HTTP_201_CREATED)

  @action(detail = True, methods = ['patch'])
  def fullfill(self, request, *args, **kwargs):
    contract = self.get_object()
    serializerContract = ContractSerializer(
      contract, 
      data={'status': 'CONCLUDED'}, 
      partial=True, 
      context={'request': request}
    )
    serializerContract.is_valid(raise_exception=True)
    serializerContract.save()

    try:
      pilot = get_object_or_404(Pilot, pk=contract.pilot.pk)
      originPlanet = pilot.locationPlanet
      initialCredits = pilot.credits
      serializer = PilotSerializer(
        pilot, 
        data={'credits': pilot.credits+contract.value, 'locationPlanet': contract.destinationPlanet}, 
        partial=True,
        context={'request': request}
      )     
      serializer.is_valid(raise_exception=True)
      serializer.save()
    except Exception as e:
      serializerRollback = ContractSerializer(
        contract, 
        data={'status': 'ACCEPTED'}, 
        partial=True, 
        context={'request': request}
      )
      serializerRollback.is_valid(raise_exception=True)
      serializerRollback.save()
      return Response(e.args, status = status.HTTP_400_BAD_REQUEST)

    try:
      ship = pilot.ship
      serializer = ShipSerializer(
        ship,
        data={'fuelLevel': ship.fuelLevel  },
        partial=True,
        context={'request': request}
      )
    except Exception as e:
      serializerRollback = ContractSerializer(
        contract, 
        data={'status': 'ACCEPTED'}, 
        partial=True, 
        context={'request': request}
      )
      serializerRollback.is_valid(raise_exception=True)
      serializerRollback.save()

      serializerRollback = PilotSerializer(
        pilot, 
        data={'credits': initialCredits, 'locationPlanet': originPlanet}, 
        partial=True,
        context={'request': request}
      )     
      serializerRollback.is_valid(raise_exception=True)
      serializerRollback.save()
      return Response(e.args, status = status.HTTP_400_BAD_REQUEST)

    return Response(serializerContract.data, status = status.HTTP_202_ACCEPTED)

class ReportTotalWeightByPlanetView(APIView):
  def get(self, request):
    queryset = Contract.objects.filter(status='CONCLUDED')
    serializer = ContractSerializer(queryset, many=True, context={'request': request})
    renderer = JSONRenderer()
    contractsConcluded = renderer.render(serializer.data)
    
    resourceDict = { resource:0 for resource in RESOURCES }
    initReducer = {planet:{'sent':resourceDict,'received':resourceDict} for planet in PLANETS}
    reducer = reduce(totalWeightReportReducer, json.loads(contractsConcluded),initReducer)
  
    return Response(reducer, status = status.HTTP_200_OK)