from django.contrib import admin
from .models import *

admin.site.register(Pilot)
admin.site.register(Ship)
admin.site.register(Resource)
admin.site.register(ResourceList)
admin.site.register(Contract)
admin.site.register(Transaction)
