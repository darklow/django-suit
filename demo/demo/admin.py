from django.contrib import admin

from .models import *
from .views import *


admin.site.site_header = 'Django Suit'


class CountryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Country, CountryAdmin)


class ContinentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Continent, CountryAdmin)
