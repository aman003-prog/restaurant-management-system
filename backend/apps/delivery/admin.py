from django.contrib import admin
from .models import DeliveryAssignment, DeliveryPartner

# Register your models here.
admin.site.register(DeliveryPartner)
admin.site.register(DeliveryAssignment)
