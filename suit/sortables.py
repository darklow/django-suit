from copy import deepcopy, copy
from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.contrib.contenttypes.admin import GenericTabularInline, GenericStackedInline
from django.forms import ModelForm, NumberInput
from django.db import models


class SortableModelAdminBase(object):
    """
    Base class for SortableTabularInline and SortableModelAdmin
    """
    sortable = 'order'

    class Media:
        js = ('suit/js/suit.sortables.js',)


class SortableListForm(ModelForm):
    """
    Just Meta holder class
    """

    class Meta:
        widgets = {
            'order': NumberInput(
                attrs={'class': 'hidden-xs-up suit-sortable'})
        }


class SortableChangeList(ChangeList):
    """
    Class that forces ordering by sortable param only
    """

    def get_ordering(self, request, queryset):
        if self.model_admin.sortable_is_enabled():
            return [self.model_admin.sortable, '-' + self.model._meta.pk.name]
        return super(SortableChangeList, self).get_ordering(request, queryset)


class SortableTabularInlineBase(SortableModelAdminBase):
    """
    Sortable tabular inline
    """

    def __init__(self, *args, **kwargs):
        super(SortableTabularInlineBase, self).__init__(*args, **kwargs)

        self.ordering = (self.sortable,)
        self.fields = self.fields or []
        if self.fields and self.sortable not in self.fields:
            self.fields = list(self.fields) + [self.sortable]

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == self.sortable:
            kwargs['widget'] = SortableListForm.Meta.widgets['order']
        return super(SortableTabularInlineBase, self).formfield_for_dbfield(
            db_field, **kwargs)


class SortableTabularInline(SortableTabularInlineBase, admin.TabularInline):
    pass


class SortableGenericTabularInline(SortableTabularInlineBase,
                                   GenericTabularInline):
    pass


class SortableStackedInlineBase(SortableModelAdminBase):
    """
    Sortable stacked inline
    """

    def __init__(self, *args, **kwargs):
        super(SortableStackedInlineBase, self).__init__(*args, **kwargs)
        self.ordering = (self.sortable,)

    def get_fieldsets(self, *args, **kwargs):
        """
        Iterate all fieldsets and make sure sortable is in the first fieldset
        Remove sortable from every other fieldset, if by some reason someone
        has added it
        """
        fieldsets = super(SortableStackedInlineBase, self).get_fieldsets(*args, **kwargs)

        sortable_added = False
        for fieldset in fieldsets:
            for line in fieldset:
                if not line or not isinstance(line, dict):
                    continue

                fields = line.get('fields')
                if self.sortable in fields:
                    fields.remove(self.sortable)

                # Add sortable field always as first
                if not sortable_added:
                    fields.insert(0, self.sortable)
                    sortable_added = True
                    break

        return fieldsets

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == self.sortable:
            kwargs['widget'] = deepcopy(SortableListForm.Meta.widgets['order'])
            kwargs['widget'].attrs['class'] += ' suit-sortable-stacked'
            kwargs['widget'].attrs['rowclass'] = ' suit-sortable-stacked-row'
        return super(SortableStackedInlineBase, self).formfield_for_dbfield(db_field, **kwargs)


class SortableStackedInline(SortableStackedInlineBase, admin.StackedInline):
    pass


class SortableGenericStackedInline(SortableStackedInlineBase,
                                   GenericStackedInline):
    pass


class SortableModelAdmin(SortableModelAdminBase, admin.ModelAdmin):
    """
    Sortable change list
    """

    def __init__(self, *args, **kwargs):
        super(SortableModelAdmin, self).__init__(*args, **kwargs)

        # Keep originals for restore
        self._original_ordering = copy(self.ordering)
        self._original_list_display = copy(self.list_display)
        self._original_list_editable = copy(self.list_editable)
        self._original_exclude = copy(self.exclude)
        self._original_list_per_page = self.list_per_page

        self.enable_sortable()

    def merge_form_meta(self, form):
        """
        Prepare Meta class with order field widget
        """
        if not getattr(form, 'Meta', None):
            form.Meta = SortableListForm.Meta
        if not getattr(form.Meta, 'widgets', None):
            form.Meta.widgets = {}
        form.Meta.widgets[self.sortable] = SortableListForm.Meta.widgets[
            'order']

    def get_changelist_form(self, request, **kwargs):
        form = super(SortableModelAdmin, self).get_changelist_form(request,
                                                                   **kwargs)
        self.merge_form_meta(form)
        return form

    def get_changelist(self, request, **kwargs):
        return SortableChangeList

    def enable_sortable(self):
        self.list_per_page = 500
        self.ordering = (self.sortable,)
        if self.list_display and self.sortable not in self.list_display:
            self.list_display = list(self.list_display) + [self.sortable]

        self.list_editable = self.list_editable or []
        if self.sortable not in self.list_editable:
            self.list_editable = list(self.list_editable) + [self.sortable]

        self.exclude = self.exclude or []
        if self.sortable not in self.exclude:
            self.exclude = list(self.exclude) + [self.sortable]

    def disable_sortable(self):
        if not self.sortable_is_enabled():
            return
        self.ordering = self._original_ordering
        self.list_display = self._original_list_display
        self.list_editable = self._original_list_editable
        self.exclude = self._original_exclude
        self.list_per_page = self._original_list_per_page

    def sortable_is_enabled(self):
        return self.list_display and self.sortable in self.list_display

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
