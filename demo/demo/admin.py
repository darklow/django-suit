from django.contrib import admin
from django.forms import ModelForm
from suit import apps
from suit.widgets import AutosizedTextarea
from .models import *
from .views import *

admin.site.site_header = 'Django Suit'


class CountryForm(ModelForm):
    class Meta:
        widgets = {
            # 'code': TextInput(attrs={'class': 'input-mini'}),
            # 'independence_day': SuitDateWidget,
            # 'area': EnclosedInput(prepend='icon-globe', append='km<sup>2</sup>',
            #                       attrs={'class': 'input-small'}),
            # 'population': EnclosedInput(prepend='icon-user',
            #                             append='<input type="button" '
            #                                    'class="btn" onclick="window'
            #                                    '.open(\'https://www.google'
            #                                    '.com/\')" value="Search">',
            #                             attrs={'class': 'input-small'}),
            'description': AutosizedTextarea,
            'architecture': AutosizedTextarea,
        }


class CountryAdmin(admin.ModelAdmin):
    form = CountryForm
    search_fields = ('name', 'code')
    list_display = ('name', 'code', 'continent', 'independence_day')
    list_filter = ('continent',)
    list_select_related = True
    date_hierarchy = 'independence_day'

    # fields = ('name', 'continent', 'code', 'independence_day')
    fieldsets = [
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ['name', 'code', 'continent', 'independence_day']
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
        'fields': {
            'code': apps.SUIT_FORM_SIZE_INLINE
        },
        'widgets': {
            'AutosizedTextarea': apps.SUIT_FORM_SIZE_XXX_LARGE,
        },
    }

    # fields = (('name', 'code', 'continent'), 'independence_day', 'population', 'description')


admin.site.register(Country, CountryAdmin)


# Inlines for KitchenSink
class CountryInlineForm(ModelForm):
    class Meta:
        widgets = {
            # 'code': TextInput(attrs={'class': 'input-mini'}),
            # 'population': TextInput(attrs={'class': 'input-medium'}),
            # 'independence_day': SuitDateWidget,
        }


class CountryInline(admin.TabularInline):
    form = CountryInlineForm
    model = Country
    fields = ('name', 'code', 'population',)
    extra = 1
    verbose_name_plural = 'Countries (Sortable example)'
    sortable = 'order'


class ContinentAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'countries')
    sortable = 'order'
    inlines = (CountryInline,)

    def countries(self, obj):
        return len(obj.country_set.all())


admin.site.register(Continent, ContinentAdmin)

class ShowcaseForm(ModelForm):
    class Meta:
        widgets = {
            'textfield': AutosizedTextarea,
        }

class ShowcaseAdmin(admin.ModelAdmin):
    form = ShowcaseForm
    # inlines = (FridgeInline, MicrowaveInline)
    search_fields = ['name']
    # radio_fields = {"horizontal_choices": admin.HORIZONTAL,
    #                 'vertical_choices': admin.VERTICAL}
    # list_editable = ('boolean',)
    # list_filter = ('choices', 'date', CountryFilter)
    list_display = ('name', 'help_text')
    readonly_fields = ('readonly_field',)
    # raw_id_fields = ('raw_id_field',)
    fieldsets = [
        (None, {'fields': ['name', 'help_text', 'textfield',
                           ('multiple_in_row', 'multiple2'),
                           'readonly_field']}),
        ('Date and time', {
            'description': 'Original Django admin date/time widgets',
            'fields': ['date_and_time', 'date', 'time_only']}),

        # ('Date and time', {
        #     'description': 'Improved date/time widgets (SuitDateWidget, '
        #                    'SuitSplitDateTimeWidget) . Uses original JS.',
        #     'fields': ['date_widget', 'datetime_widget']}),

        # ('Foreign key relations',
        #  {'description': 'Original select and linked select feature',
        #   'fields': ['country', 'linked_foreign_key', 'raw_id_field']}),
        #
        # ('EnclosedInput widget',
        #  {
        #      'description': 'Supports Twitter Bootstrap prepended, '
        #                     'appended inputs',
        #      'fields': ['enclosed1', 'enclosed2']}),
        #
        # ('Boolean and choices',
        #  {'fields': ['boolean', 'boolean_with_help', 'choices',
        #              'horizontal_choices', 'vertical_choices']}),
        #
        # ('Collapsed settings', {
        #     'classes': ('collapse',),
        #     'fields': ['hidden_checkbox', 'hidden_choice']}),
        # ('And one more collapsable', {
        #     'classes': ('collapse',),
        #     'fields': ['hidden_charfield', 'hidden_charfield2']}),

    ]
    suit_form_size = {
        # 'fields': {
        #     'code': apps.SUIT_FORM_SIZE_INLINE
        # },
        'widgets': {
            # 'AutosizedTextarea': apps.SUIT_FORM_SIZE_XXX_LARGE,
        },
    }
    # list_display = ('name', 'help_text', 'choices', 'horizontal_choices', 'boolean')


admin.site.register(Showcase, ShowcaseAdmin)
