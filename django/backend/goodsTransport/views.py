from goodsTransport.serializers import PilotSerializer, ShipSerializer, ContractSerializer
from goodsTransport.models import Pilot, Ship, Contract
from rest_framework import viewsets

class PilotViewSet(viewsets.ModelViewSet):
  queryset = Pilot.objects.all()
  serializer_class = PilotSerializer

class ShipViewSet(viewsets.ModelViewSet):
  queryset = Ship.objects.all()
  serializer_class = ShipSerializer

class ContractViewSet(viewsets.ModelViewSet):
  queryset = Contract.objects.all()
  serializer_class = ContractSerializer
