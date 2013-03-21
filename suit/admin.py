from django.contrib.contenttypes.models import ContentType
from django.template.response import TemplateResponse
from django.utils.safestring import mark_safe
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


class TabbedModelAdmin(ModelAdmin):
    """
    The same as ModelAdmin, except the fieldsets are rendered as tabs
    """

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        """
        Almost the same method as in the superclass, but the templates are different. Maybe a cleaner solution is possible.
        """
        opts = self.model._meta
        app_label = opts.app_label
        ordered_objects = opts.get_ordered_objects()
        context.update({
            'add': add,
            'change': change,
            'has_add_permission': self.has_add_permission(request),
            'has_change_permission': self.has_change_permission(request, obj),
            'has_delete_permission': self.has_delete_permission(request, obj),
            'has_file_field': True,
            'has_absolute_url': hasattr(self.model, 'get_absolute_url'),
            'ordered_objects': ordered_objects,
            'form_url': mark_safe(form_url),
            'opts': opts,
            'content_type_id': ContentType.objects.get_for_model(self.model).id,
            'save_as': self.save_as,
            'save_on_top': self.save_on_top,
        })
        if add and self.add_form_template is not None:
            form_template = self.add_form_template
        else:
            form_template = self.change_form_template

        return TemplateResponse(request, form_template or [
            "suit/%s/%s/tabbed_change_form.html" % (app_label, opts.object_name.lower()),
            "suit/%s/tabbed_change_form.html" % app_label,
            "suit/tabbed_change_form.html"
        ], context, current_app=self.admin_site.name)



