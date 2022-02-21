from django.core.exceptions import ValidationError

def validate_age(value):
  if value < 18:
    raise ValidationError(
      ('Age must be at least 18.'),
      params={'value': value},
    )