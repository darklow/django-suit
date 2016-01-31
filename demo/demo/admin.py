from django.contrib import admin

from .models import *
from .views import *


admin.site.site_header = 'Django Suit'


class CountryAdmin(admin.ModelAdmin):
    search_fields = ('name', 'code')
    list_display = ('name', 'code', 'continent', 'independence_day')
    list_filter = ('continent',)
    list_select_related = True
    date_hierarchy = 'independence_day'
    fields = (('name', 'code', 'continent'), 'independence_day', 'population', 'description')


admin.site.register(Country, CountryAdmin)


class ContinentAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'countries')
    sortable = 'order'

    def countries(self, obj):
        return len(obj.country_set.all())

admin.site.register(Continent, ContinentAdmin)
