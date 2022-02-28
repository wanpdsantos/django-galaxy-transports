from goodsTransport.models import *
import factory

class PilotFactory(factory.django.DjangoModelFactory ):
  class Meta:
    model = Pilot

  pilotCertification = factory.Sequence(int)
  name = factory.Faker("name")
  age = 20
  credits = 20

class ShipFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Ship
  
  fuelCapacity = 100
  fuelLevel = 100
  weightCapacity = 100

class ResourceListFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = ResourceList

class ResourceFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Resource
  
  name='FOOD'
  weight=10.59

class ContractFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Contract
  
  originPlanet = 'CALAS'
  destinationPlanet = 'ANDVARI'
  value = 15.5

class TransactionFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Transaction

  description = factory.Faker("sentence")
