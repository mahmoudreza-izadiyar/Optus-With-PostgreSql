from django.contrib import admin
from .models import Cars


class CarsAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'model', 'photo', 'binaryPhoto')


admin.site.register(Cars, CarsAdmin)