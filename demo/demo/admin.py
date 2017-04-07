from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.forms import ModelForm, Select, TextInput, NumberInput
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.shortcuts import redirect
from django_select2.forms import ModelSelect2Widget
from suit import apps

from suit.admin import RelatedFieldAdmin, get_related_field
from suit.admin_filters import IsNullFieldListFilter
from suit.sortables import SortableTabularInline, SortableModelAdmin, SortableStackedInline
from suit.widgets import AutosizedTextarea, EnclosedInput
from .widgets import Bootstrap4Select
from .models import *
from .views import *

admin.site.site_header = 'Django Suit'


class CityInlineForm(ModelForm):
    class Meta:
        widgets = {
            'area': EnclosedInput(prepend='fa-globe', append='km<sup>2</sup>'),
            'population': EnclosedInput(prepend='fa-users'),
        }


class CityInline(admin.TabularInline):
    form = CityInlineForm
    model = City
    min_num = 3
    extra = 0
    verbose_name_plural = 'Cities'
    suit_classes = 'suit-tab suit-tab-cities'
    suit_form_inlines_hide_original = True


class CountryForm(ModelForm):
    class Meta:
        widgets = {
            # 'code': TextInput(attrs={'class': 'input-mini'}),
            # 'independence_day': SuitDateWidget,
            'area': EnclosedInput(prepend='fa-globe', append='km<sup>2</sup>',
                                  attrs={'placeholder': 'Country area'}),
            'population': EnclosedInput(
                prepend='fa-users',
                append='<button class="btn btn-secondary" type="button" '
                       'onclick="window.open(\'https://www.google.com/\')">Search</button>',
                append_class='btn', attrs={'placeholder': 'Human population'}),
            'description': AutosizedTextarea,
            'architecture': AutosizedTextarea,
        }


class PopulationFilter(IsNullFieldListFilter):
    notnull_label = 'With population data'
    isnull_label = 'Missing population data'
    # def __init__(self, *args, **kwargs):
    #     super(ContinentFilter, self).__init__(*args, **kwargs)
    #     self.title = 'override filter title'


@admin.register(Country)
class CountryAdmin(RelatedFieldAdmin):
    form = CountryForm
    search_fields = ('name', 'code')
    list_display = ('name', 'code', 'link_to_continent', 'independence_day')
    list_filter = ('continent', 'independence_day', 'code', ('population', PopulationFilter))
    suit_list_filter_horizontal = ('code', 'population')
    list_select_related = True
    inlines = (CityInline,)
    # date_hierarchy = 'independence_day'

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
            'code': apps.SUIT_FORM_SIZE_INLINE,
            'area': apps.SUIT_FORM_SIZE_SMALL,
            'population': apps.SUIT_FORM_SIZE_SMALL,
        },
        'widgets': {
            'AutosizedTextarea': apps.SUIT_FORM_SIZE_XXX_LARGE,
        },
    }

    suit_form_tabs = (
        ('general', 'General'),
        ('cities', 'Cities'),
        ('flag', 'Flag'),
        ('charts', 'Charts'),
        ('info', 'Info on tabs')
    )

    suit_form_includes = (
        ('admin/demo/country/tab_notice.html', 'middle', 'cities'),
        ('admin/demo/country/tab_flag.html', '', 'flag'),
        ('admin/demo/country/tab_charts.html', '', 'charts'),
        ('admin/demo/country/tab_docs.html', '', 'info'),
    )


# Inlines for ContinentAdmin
class CountryInlineForm(ModelForm):
    class Meta:
        widgets = {
            # 'code': TextInput(attrs={'class': 'input-mini'}),
            # 'population': TextInput(attrs={'class': 'input-medium'}),
            # 'independence_day': SuitDateWidget,
        }


class CountryInline(SortableTabularInline):
    form = CountryInlineForm
    model = Country
    fields = ('name', 'code', 'population', 'continent')
    extra = 1
    verbose_name_plural = 'Countries (Sortable example)'
    sortable = 'order'
    show_change_link = True


@admin.register(Continent)
class ContinentAdmin(SortableModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'countries')
    sortable = 'order'
    inlines = (CountryInline,)

    def suit_row_attributes(self, obj, request):
        class_map = {
            'Europe': 'table-success',
            'South America': 'table-warning',
            'North America': 'table-success',
            'Africa': 'table-danger',
            'Australia': 'table-warning',
            'Asia': 'table-info',
            'Antarctica': 'table-info',
        }

        css_class = class_map.get(obj.name)
        if css_class:
            return {'class': css_class}

    def suit_column_attributes(self, column):
        if column == 'countries':
            return {'class': 'text-xs-center'}

    def suit_cell_attributes(self, obj, column):
        if column == 'countries':
            cls = 'text-xs-center'
            if obj.name == 'Antarctica':
                cls += ' table-danger'
            return {'class': cls}

    def countries(self, obj):
        return len(obj.country_set.all())


class BookInline(SortableTabularInline):
    model = Book
    min_num = 1
    extra = 0
    verbose_name_plural = 'Books (Tabular inline)'
    suit_form_inlines_hide_original = True


class MovieInlineForm(ModelForm):
    class Meta:
        fields = '__all__'
        model = Movie
        widgets = {
            'description': AutosizedTextarea(attrs={'rows': 2}),
            'type': Select(attrs={'class': 'input-small'}),
        }


class MovieInline(SortableStackedInline):
    model = Movie
    form = MovieInlineForm
    min_num = 1
    extra = 0
    verbose_name_plural = 'Movies (Stacked inline)'
    fields = ['title', 'description', 'rating', 'is_released']
    suit_form_size = {
        'default': apps.SUIT_FORM_SIZE_X_LARGE,
    }


class CountrySelect2Widget(Bootstrap4Select, ModelSelect2Widget):
    search_fields = [
        'name__icontains',
        'code__iexact',
    ]


class ColorInput(TextInput):
    input_type = 'color'


class DateInput(TextInput):
    input_type = 'date'


class ShowcaseForm(ModelForm):
    class Meta:
        widgets = {
            'html5_color': ColorInput,
            'html5_number': NumberInput,
            'html5_date': DateInput,
            'textfield': AutosizedTextarea,
            'country2': CountrySelect2Widget()
        }


@admin.register(Showcase)
class ShowcaseAdmin(RelatedFieldAdmin):
    form = ShowcaseForm
    inlines = (BookInline, MovieInline)
    search_fields = ['name']
    # radio_fields = {"horizontal_choices": admin.HORIZONTAL,
    #                 'vertical_choices': admin.VERTICAL}
    # list_editable = ('boolean',)
    list_filter = ('choices', 'vertical_choices')
    suit_list_filter_horizontal = ('choices',)
    # list_display = ('name', 'help_text', 'choices', 'horizontal_choices', 'boolean')
    list_display = ('name', 'help_text', 'link_to_country__continent')
    readonly_fields = ('readonly_field', 'link_to_country')
    radio_fields = {"horizontal_choices": admin.HORIZONTAL,
                    'vertical_choices': admin.VERTICAL}
    raw_id_fields = ('raw_id_field',)

    # Optional: Use following to override short_description or admin_order_field if needed
    link_to_country__continent = get_related_field(
        'link_to_country__continent', short_description='Continent (2nd level FK link)')
    link_to_country = get_related_field('link_to_country')

    fieldsets = [
        (None, {'fields': ['name', 'help_text', 'textfield',
                           ('multiple_in_row', 'multiple2'),
                           'readonly_field']}),
        ('Date and time', {
            'description': 'Original Django admin date/time widgets',
            'fields': ['date_and_time', 'date', 'time_only']}),
        ('Native HTML5 inputs', {
            'description': 'Some HTML5 inputs are still not supported by IE!',
            'fields': ['html5_color', 'html5_number', 'html5_date']}),

        ('Collapsed settings', {
            'classes': ('collapse',),
            'fields': ['collapsed_param']}),

        ('Boolean and choices',
         {'fields': ['boolean', 'boolean_with_help', 'choices',
                     'horizontal_choices', 'vertical_choices']}),

        ('Foreign key relations',
         {'description': 'Original select and linked select feature',
          'fields': ['link_to_country', 'country', 'country2', 'raw_id_field']}),

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

    def get_urls(self):
        """
        Example how to extend Django ModelAdmin with extra actions and views
        """
        urls = super(ShowcaseAdmin, self).get_urls()
        my_urls = [
            url(r'^(\d+)/clickme/$', showcase_custom_view_example, name='demo_showcase_clickme')
        ]
        return my_urls + urls


@staff_member_required
def showcase_custom_view_example(request, pk):
    instance = Showcase.objects.get(pk=pk)

    # Do something legendary here
    messages.success(request, 'Something legendary was done to "%s"' % instance)

    return redirect('admin:demo_showcase_change', pk)
