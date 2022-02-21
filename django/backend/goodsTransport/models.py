from django.db import models
from .validators import validate_age

class Pilot(models.Model):
  pilotCertification = models.CharField(max_length=7, primary_key=True)
  name = models.CharField(max_length=100, blank=False, null=False)
  age = models.IntegerField(validators=[validate_age], blank=False, null=False)
  credits = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
  locationPlanet = models.CharField(max_length=100, blank=True, null=True)
      
  