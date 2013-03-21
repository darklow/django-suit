import suit.config
from django.contrib.admin import ModelAdmin
from django.contrib.admin.views.main import ChangeList
from django.forms import ModelForm
from django.contrib import admin
from django.db import models
from suit.widgets import NumberInput


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

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == self.sortable:
            kwargs['widget'] = SortableListForm.Meta.widgets['order']
        return super(SortableTabularInline, self).formfield_for_dbfield(
            db_field, **kwargs)


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

    def get_changelist(self, request, **kwargs):
        return SortableChangeList

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            max_order = obj.__class__.objects.aggregate(
                models.Max(self.sortable))
            try:
                next_order = max_order['%s__max' % self.sortable] + 1
            except TypeError:
                next_order = 1
            setattr(obj, self.sortable, next_order)
        super(SortableModelAdmin, self).save_model(request, obj, form, change)



