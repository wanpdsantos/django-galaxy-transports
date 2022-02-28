def totalWeightReportReducer(acumulator, current):
  transportPayload = acumulator[current['originPlanet']]['sent'].copy()
  for item in current['payload']:
    transportPayload[item['name']] = transportPayload[item['name']] + item['weight']
  acumulator[current['originPlanet']]['sent'] = transportPayload
  acumulator[current['destinationPlanet']]['received'] = transportPayload
  return acumulator