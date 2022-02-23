FUEL_COST_PER_UNITY = 7

PLANETS = [
  ('ANDVARI','Andvari'),
  ('AQUA','Aqua'),
  ('CALAS','Calas'),
  ('DEMETER','Demeter'),
]

ROUTES = {
  'Andvari-Demeter': {
    'allowed': False,
    'fuelCost': None
  },
  'Andvari-Aqua': {
    'allowed': True,
    'fuelCost': 13
  },
  'Andvari-Calas': {
    'allowed': True,
    'fuelCost': 23
  },
  'Demeter-Andvari': {
    'allowed': False,
    'fuelCost': None
  },
  'Demeter-Aqua': {
    'allowed': True,
    'fuelCost': 22
  },
  'Demeter-Calas': {
    'allowed': True,
    'fuelCost': 25
  },
  'Aqua-Andvari': {
    'allowed': False,
    'fuelCost': None
  },
  'Aqua-Demeter': {
    'allowed': True,
    'fuelCost': 30
  },
  'Aqua-Calas': {
    'allowed': True,
    'fuelCost': 12
  },
  'Calas-Andvari': {
    'allowed': True,
    'fuelCost': 20
  },
  'Calas-Demeter': {
    'allowed': True,
    'fuelCost': 25
  },
  'Calas-Aqua': {
    'allowed': True,
    'fuelCost': 15
  }
}