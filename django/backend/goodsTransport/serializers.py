from django.urls import reverse
from goodsTransport.models import Pilot, Ship, Contract, Resource, ResourceList
from rest_framework import serializers
from goodsTransport.constants import ROUTES

class PilotSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    fields = '__all__'
    model = Pilot
  
  def update(self, instance, validated_data, *args, **kwargs):
    request = self.context.get('request', False)
    if request and not 'ships' in request.path:
      route = f"{getattr(instance, 'locationPlanet')}-{validated_data['locationPlanet']}"
      route = ROUTES.get(route, False)

      if not route or not route['allowed']:
        raise serializers.ValidationError('Route not available.')
      if not isinstance(getattr(instance, 'ship'), Ship):
        raise serializers.ValidationError('Pilot does not have a ship. Attach a ship to the pilot before traveling.')
      if route['fuelCost'] > getattr(instance, 'ship').fuelLevel:
        raise serializers.ValidationError('Not enough fuel to travel.')

    return super(PilotSerializer, self).update(instance, validated_data)

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
    request = self.context.get('request', False)
    if request and 'ships' in request.path:
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

  def validate(self, data):
    request = self.context.get('request', False)
    if request and request.path==reverse('contract-list'):
      if data['originPlanet'].upper() == data['destinationPlanet'].upper():
        raise serializers.ValidationError('Contracts cannot have same origin and destination.')
    return data

  def to_representation(self, instance):
    response = super().to_representation(instance)
    query = Resource.objects.filter(list=instance.payload).values()
    response['payload'] = query
    return response

  def update(self, instance, validated_data):
    if(getattr(instance, 'status') == 'ACCEPTED' and validated_data['status'] == 'ACCEPTED'):
      raise serializers.ValidationError('Contract already accepted.')

    if(getattr(instance, 'status') == 'CONCLUDED' and validated_data['status'] == 'CONCLUDED'):
      raise serializers.ValidationError('Contract already concluded.')

    if(getattr(instance, 'status') == 'OPEN' and validated_data['status'] == 'CONCLUDED'):
      raise serializers.ValidationError('Cannot fullfill open contracts.')

    request = self.context.get('request', False)
    if request and 'fullfill' in request.path:
      if getattr(instance, 'originPlanet') != getattr(instance, 'pilot').locationPlanet:
        raise serializers.ValidationError('Pilot shoud be at contract origin planet to start the travel.')

    return super(ContractSerializer, self).update(instance, validated_data)