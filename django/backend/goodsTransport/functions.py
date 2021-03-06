from goodsTransport.constants import RESOURCES
from goodsTransport.serializers import TransactionSerializer

def totalWeightReportReducer(acumulator, current):
  transportPayload = acumulator[current['originPlanet']]['sent'].copy()
  for item in current['payload']:
    transportPayload[item['name']] = transportPayload[item['name']] + item['weight']
  acumulator[current['originPlanet']]['sent'] = transportPayload
  acumulator[current['destinationPlanet']]['received'] = transportPayload
  return acumulator

def pilotResourceTransportedReportReducer(acumulator, current):
  resourceList = {resource:0 for resource in RESOURCES}
  if not current['pilot'] in acumulator: acumulator[current['pilot']] = resourceList
  for item in current['payload']:
    acumulator[current['pilot']][item['name']] += item['weight']
  return acumulator

def logTransaction(request, transaction):
  try:
    serializer = TransactionSerializer(data={'description':transaction}, context={'request': request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
  except Exception as e:
    print(e)
  return None