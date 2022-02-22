from goodsTransport.models import Pilot, Ship
from rest_framework import serializers

class PilotSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    fields = '__all__'
    model = Pilot
  
  def validate_age(self, age):
    if age < 18:
      raise serializers.ValidationError('Age must be at least 18.')
    return age
  def validate_credits(self, credits):
    if credits < 0:
      raise serializers.ValidationError('Credits cannot be negative.')
    return credits

class ShipSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Ship
    fields = '__all__'
  
  def validate_fuelCapacity(self, fuelCapacity):
    if fuelCapacity < 0:
      raise serializers.ValidationError('Fuel capacity cannot be negative.')
    return fuelCapacity

  def validate_fuelLevel(self, fuelLevel):
    if fuelLevel < 0:
      raise serializers.ValidationError('Fuel level cannot be negative.')
    return fuelLevel

  def validate_weightCapacity(self, weightCapacity):
    if weightCapacity < 0:
      raise serializers.ValidationError('Weight capacity cannot be negative.')
    return weightCapacity