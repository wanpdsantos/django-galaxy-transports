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

  @action(detail = True, methods = ['post'])
  def contract(self, request, *args, **kwargs):
    if not 'contract_id' in request.data: 
      return Response({'Missing contract_id on request body.'}, status = status.HTTP_400_BAD_REQUEST)

    queryset = Contract.objects.all()
    contract = get_object_or_404(queryset, id = request.data['contract_id'])
    if isinstance(contract.pilot, Pilot): 
      return Response({'Contract already accepted.'}, status = status.HTTP_409_CONFLICT) 

    serializer = ContractSerializer(
      contract, 
      data={'status': 'ACCEPTED' , 'pilot': reverse("pilot-detail", args=[self.get_object().id]) }, 
      partial=True,
      context={'request': request}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status = status.HTTP_201_CREATED)

class ShipViewSet(viewsets.ModelViewSet):
  queryset = Ship.objects.all()
  serializer_class = ShipSerializer

  @action(detail = True, methods = ['patch'])
  def fuel(self, request, *args, **kwargs):
    queryset = Pilot.objects.all()
    pilot = get_object_or_404(queryset, pilotCertification = request.data['pilotCertification'])
    serializer = PilotSerializer(
      pilot, 
      data={'credits': pilot.credits-request.data['quantity']*FUEL_COST_PER_UNITY}, 
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
          'fuelLevel': ship.fuelLevel+request.data['quantity'],
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
        data={'credits': pilot.credits+request.data['quantity']*FUEL_COST_PER_UNITY}, 
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
      request.data['payload']
    ))
    serializer = ResourceSerializer(data=items, many=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    contract = Contract.objects.create(
      description = request.data['description'],
      originPlanet = request.data['originPlanet'],
      destinationPlanet = request.data['destinationPlanet'],
      value = request.data['value'],
      payload = newResourceList,
      status = 'OPEN',
    )
    return Response(ContractSerializer(
      contract, 
      context={'request': request}
    ).data, status = status.HTTP_201_CREATED)