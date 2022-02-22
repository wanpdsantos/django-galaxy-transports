from django.db import models
from .validators import validate_age

PLANETS = [
  ('ANDVARI','Andvari'),
  ('AQUA','Aqua'),
  ('CALAS','Calas'),
  ('DEMETER','Demeter'),
]
class Pilot(models.Model):
  pilotCertification = models.CharField(max_length=7, blank=False, null=False, unique=True)
  name = models.CharField(max_length=100, blank=False, null=False)
  age = models.IntegerField(validators=[validate_age], blank=False, null=False)
  credits = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
  locationPlanet = models.CharField(choices=PLANETS, max_length=10, blank=True, null=True)

class Ship(models.Model):
  fuelCapacity = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False)
  fuelLevel = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False)
  weightCapacity = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False)

class ResourceList(models.Model):
  id = models.BigAutoField(primary_key=True)

class Resource(models.Model):
  RESOURCES = [
    ('WATER', 'Water'),
    ('MINERALS', 'Minerals'),
    ('FOOD', 'Food'),
  ]
  name = models.CharField(max_length=10, choices=RESOURCES)
  weight = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False)
  list = models.ForeignKey(ResourceList, on_delete=models.CASCADE, blank=False, null=False)

class Contract(models.Model):
  description = models.CharField(max_length=200, blank=True, null=True)
  originPlanet = models.CharField(choices=PLANETS, max_length=10, blank=False, null=False)
  destinationPlanet = models.CharField(choices=PLANETS, max_length=10, blank=False, null=False)
  value = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False)
  payload = models.ForeignKey(ResourceList, on_delete=models.CASCADE, blank=False, null=False)









  