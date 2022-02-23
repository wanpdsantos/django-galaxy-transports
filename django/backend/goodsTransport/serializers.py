from goodsTransport.models import Pilot, Ship, Contract, Resource, ResourceList
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
      raise serializers.ValidationError('Insufficient credits to perform this operation.')
    return credits
  

class ShipSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Ship
    fields = '__all__'
  
  def validate(self, data):
    if data['fuelLevel'] > data['fuelCapacity']:
      raise serializers.ValidationError('Max fuel level reached.')
    return data

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

class ResourceSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Resource
    fields = '__all__'

  def validate_weight(self, weight):
    if weight < 0:
      raise serializers.ValidationError('Weight cannot be less than zero.')
    return weight

class ResourceListSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = ResourceList
    fields = '__all__'

class ContractSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Contract
    fields = '__all__'

  def to_representation(self, instance):
    response = super().to_representation(instance)
    query = Resource.objects.filter(list=instance.payload).values()
    response['payload'] = query
    return response