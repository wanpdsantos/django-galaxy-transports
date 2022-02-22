from goodsTransport.serializers import PilotSerializer, ShipSerializer
from goodsTransport.models import Pilot, Ship
from rest_framework import viewsets

class PilotViewSet(viewsets.ModelViewSet):
  queryset = Pilot.objects.all()
  serializer_class = PilotSerializer

class ShipViewSet(viewsets.ModelViewSet):
  queryset = Ship.objects.all()
  serializer_class = ShipSerializer