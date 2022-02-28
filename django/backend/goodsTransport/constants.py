FUEL_COST_PER_UNITY = 7

PLANETS = [
  'ANDVARI',
  'AQUA',
  'CALAS',
  'DEMETER',
]

RESOURCES = [
  'FOOD', 
  'MINERALS', 
  'WATER'
]

ROUTES = {
  'ANDVARI-DEMETER': {
    'allowed': False,
    'fuelCost': None
  },
  'ANDVARI-AQUA': {
    'allowed': True,
    'fuelCost': 13
  },
  'ANDVARI-CALAS': {
    'allowed': True,
    'fuelCost': 23
  },
  'DEMETER-ANDVARI': {
    'allowed': False,
    'fuelCost': None
  },
  'DEMETER-AQUA': {
    'allowed': True,
    'fuelCost': 22
  },
  'DEMETER-CALAS': {
    'allowed': True,
    'fuelCost': 25
  },
  'AQUA-ANDVARI': {
    'allowed': False,
    'fuelCost': None
  },
  'AQUA-DEMETER': {
    'allowed': True,
    'fuelCost': 30
  },
  'AQUA-CALAS': {
    'allowed': True,
    'fuelCost': 12
  },
  'CALAS-ANDVARI': {
    'allowed': True,
    'fuelCost': 20
  },
  'CALAS-DEMETER': {
    'allowed': True,
    'fuelCost': 25
  },
  'CALAS-AQUA': {
    'allowed': True,
    'fuelCost': 15
  }
}