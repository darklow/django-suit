from django.contrib import admin
from suit import apps
from .models import *
from .views import *


admin.site.site_header = 'Django Suit'


class CountryAdmin(admin.ModelAdmin):
    search_fields = ('name', 'code')
    list_display = ('name', 'code', 'continent', 'independence_day')
    list_filter = ('continent',)
    list_select_related = True
    date_hierarchy = 'independence_day'
    # fields = ('name', 'continent', 'code', 'independence_day')
    fieldsets = [
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ['name', 'continent', 'code', 'independence_day']
        }),
        ('Statistics', {
            'classes': ('suit-tab suit-tab-general',),
            'description': 'EnclosedInput widget examples',
            'fields': ['area', 'population']}),
        ('Autosized textarea', {
            'classes': ('suit-tab suit-tab-general',),
            'description': 'AutosizedTextarea widget example - adapts height '
                           'based on user input',
            'fields': ['description']}),
        ('Architecture', {
            'classes': ('suit-tab suit-tab-cities',),
            'description': 'Tabs can contain any fieldsets and inlines',
            'fields': ['architecture']}),
    ]

    suit_form_size = {
        'widgets': {
            'AdminTextareaWidget': apps.SUIT_FORM_SIZE_XX_LARGE
        },
    }

    # fields = (('name', 'code', 'continent'), 'independence_day', 'population', 'description')
#

admin.site.register(Country, CountryAdmin)


class ContinentAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'countries')
    sortable = 'order'

    def countries(self, obj):
        return len(obj.country_set.all())

admin.site.register(Continent, ContinentAdmin)
