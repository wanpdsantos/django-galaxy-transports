from goodsTransport.models import Pilot
import factory

class PilotFactory(factory.django.DjangoModelFactory ):
  class Meta:
    model = Pilot

  name = factory.Faker("name")
  age = 20