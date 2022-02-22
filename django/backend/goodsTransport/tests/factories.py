from goodsTransport.models import *
import factory

class PilotFactory(factory.django.DjangoModelFactory ):
  class Meta:
    model = Pilot

  name = factory.Faker("name")
  age = 20

class ShipFactory(factory.django.DjangoModelFactory ):
  class Meta:
    model = Ship
  
  fuelCapacity = 10
  fuelLevel = 5
  weightCapacity = 10
