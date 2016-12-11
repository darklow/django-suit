from django.conf.urls import url
from django.contrib import admin
from django.forms import ModelForm, Select
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.shortcuts import redirect

from suit import apps
from suit.sortables import SortableTabularInline, SortableModelAdmin, SortableStackedInline
from suit.widgets import AutosizedTextarea
from .models import *
from .views import *

admin.site.site_header = 'Django Suit'


class CityInlineForm(ModelForm):
    class Meta:
        widgets = {
            # 'area': EnclosedInput(prepend='icon-globe', append='km<sup>2</sup>',
            #                       attrs={'class': 'input-small'}),
            # 'population': EnclosedInput(append='icon-user',
            #                             attrs={'class': 'input-small'}),
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
    # date_hierarchy = 'independence_day'
    inlines = (CityInline,)

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


    # fields = (('name', 'code', 'continent'), 'independence_day', 'population', 'description')


admin.site.register(Country, CountryAdmin)


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


class ContinentAdmin(SortableModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'countries')
    sortable = 'order'
    inlines = (CountryInline,)

    def suit_row_attributes(self, obj):
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


admin.site.register(Continent, ContinentAdmin)


class ShowcaseForm(ModelForm):
    class Meta:
        widgets = {
            'textfield': AutosizedTextarea,
        }


@staff_member_required
def showcase_custom_view_example(request, pk):
    instance = Showcase.objects.get(pk=pk)

    # Do something legendary here
    messages.success(request, 'Something legendary was done to "%s"' % instance)

    return redirect('admin:demo_showcase_change', pk)


# Inlines for Showcase
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


class ShowcaseAdmin(admin.ModelAdmin):
    form = ShowcaseForm
    inlines = (BookInline, MovieInline)
    search_fields = ['name']
    # radio_fields = {"horizontal_choices": admin.HORIZONTAL,
    #                 'vertical_choices': admin.VERTICAL}
    # list_editable = ('boolean',)
    # list_filter = ('choices', 'date', CountryFilter)
    # list_display = ('name', 'help_text', 'choices', 'horizontal_choices', 'boolean')
    list_display = ('name', 'help_text')
    readonly_fields = ('readonly_field',)
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

    def get_urls(self):
        """
        Example how to extend Django ModelAdmin with extra actions and views
        """
        urls = super(ShowcaseAdmin, self).get_urls()
        my_urls = [
            url(r'^(\d+)/clickme/$', showcase_custom_view_example, name='demo_showcase_clickme')
        ]
        return my_urls + urls


admin.site.register(Showcase, ShowcaseAdmin)
