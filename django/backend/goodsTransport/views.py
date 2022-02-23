from django.urls import reverse
from django.shortcuts import get_object_or_404
from goodsTransport.serializers import PilotSerializer, ShipSerializer, ContractSerializer, ResourceSerializer, ResourceListSerializer
from goodsTransport.models import Pilot, Ship, Contract, ResourceList, Resource
from goodsTransport.constants import FUEL_COST_PER_UNITY
from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from rest_framework.decorators import action

class PilotViewSet(viewsets.ModelViewSet):
  queryset = Pilot.objects.all()
  serializer_class = PilotSerializer

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

    contract = Contract.objects.create(
      description = request.data.get('description'),
      originPlanet = request.data.get('originPlanet'),
      destinationPlanet = request.data.get('destinationPlanet'),
      value = request.data.get('value'),
      payload = newResourceList,
      status = 'OPEN',
    )
    return Response(ContractSerializer(
      contract, 
      context={'request': request}
    ).data, status = status.HTTP_201_CREATED)