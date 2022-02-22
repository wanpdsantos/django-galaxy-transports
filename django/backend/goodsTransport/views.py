from django.urls import reverse
from goodsTransport.serializers import PilotSerializer, ShipSerializer, ContractSerializer, ResourceSerializer, ResourceListSerializer
from goodsTransport.models import Pilot, Ship, Contract, ResourceList, Resource
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

class PilotViewSet(viewsets.ModelViewSet):
  queryset = Pilot.objects.all()
  serializer_class = PilotSerializer

class ShipViewSet(viewsets.ModelViewSet):
  queryset = Ship.objects.all()
  serializer_class = ShipSerializer

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
      lambda item: {'list': reverse("resourcelist-detail", args=[newResourceList.id]), 'name': item['name'], 'weight': item['weight']} , 
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
      payload = newResourceList
    )
    return Response(ContractSerializer(contract, context={'request': request}).data, status = status.HTTP_201_CREATED)