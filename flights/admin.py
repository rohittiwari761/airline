from django.contrib import admin
from .models import Airport,flight,passenger
# Register your models here.

admin.site.register(Airport)
admin.site.register(flight)
admin.site.register(passenger)
