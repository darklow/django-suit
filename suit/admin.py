from django.contrib.admin import ModelAdmin
from django.contrib.admin.views.main import ChangeList, ORDER_VAR
from django.forms import ModelForm, TextInput, HiddenInput
from inspect import stack
from pprint import pprint
from suit.widgets import NumberInput
from django.contrib import admin


class SortableModelAdminBase(object):
    """
    Base class for SortableTabularInline and SortableModelAdmin
    """
    sortable = 'order'
    class Media:
        js = ('suit/js/sortables.js',)


class SortableListForm(ModelForm):
    """
    Just Meta holder class
    """
    class Meta:
        widgets = {
            'order': NumberInput(
                attrs={'class': 'hide input-mini suit-sortable'})
        }


class SortableChangeList(ChangeList):
    """
    Class that forces ordering by sortable param only
    """

    def get_ordering(self, request, queryset):
        return [self.model_admin.sortable, '-' + self.model._meta.pk.name]


class SortableTabularInline(SortableModelAdminBase, admin.TabularInline):
    """
    Sortable tabular inline
    """

    def __init__(self, *args, **kwargs):
        super(SortableTabularInline, self).__init__(*args, **kwargs)

        self.ordering = (self.sortable,)
        self.fields = self.fields or []
        if self.fields and self.sortable not in self.fields:
            self.fields = list(self.fields) + [self.sortable]

        self.form.Meta.widgets[self.sortable] = SortableListForm.Meta.widgets[
            'order']


class SortableModelAdmin(SortableModelAdminBase, ModelAdmin):
    """
    Sortable tabular inline
    """
    list_per_page = 500

    def __init__(self, *args, **kwargs):
        super(SortableModelAdmin, self).__init__(*args, **kwargs)

        self.ordering = (self.sortable,)
        if self.list_display and self.sortable not in self.list_display:
            self.list_display = list(self.list_display) + [self.sortable]

        self.list_editable = self.list_editable or []
        if self.sortable not in self.list_editable:
            self.list_editable = list(self.list_editable) + [self.sortable]

        self.exclude = self.exclude or []
        if self.sortable not in self.exclude:
            self.exclude = list(self.exclude) + [self.sortable]

        self.prepare_form()

    def prepare_form(self):
        """
        Merge originally defined form if any and prepare Meta class widgets
        """
        if not getattr(self.form, 'Meta', None):
            self.form.Meta = SortableListForm.Meta
        if not getattr(self.form.Meta, 'widgets', None):
            self.form.Meta.widgets = {}
        self.form.Meta.widgets[self.sortable] = SortableListForm.Meta.widgets[
            'order']
        # Store reference to form class, to use in get_changelist_form()
        self._form = self.form

    def get_changelist_form(self, request, **kwargs):
        kwargs.setdefault('form', self._form)
        return super(SortableModelAdmin, self).get_changelist_form(request,
                                                                   **kwargs)
    def get_changelist_formset(self, request, **kwargs):
        formset = super(SortableModelAdmin, self).get_changelist_formset(
            request, **kwargs)
        return formset

    def get_changelist(self, request, **kwargs):
        return SortableChangeList

