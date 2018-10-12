from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe
try:
    from django.urls import reverse_lazy
except:
    from django.core.urlresolvers import reverse_lazy

"""
Adapted by using following examples:
https://djangosnippets.org/snippets/2887/
http://stackoverflow.com/a/7192721/641263
"""

link_to_prefix = 'link_to_'


def get_admin_url(instance, admin_prefix='admin', current_app=None):
    if not instance.pk:
        return
    return reverse_lazy(
        '%s:%s_%s_change' % (admin_prefix, instance._meta.app_label, instance._meta.model_name),
        args=(instance.pk,),
        current_app=current_app
    )


def get_related_field(name, short_description=None, admin_order_field=None, admin_prefix='admin'):
    """
    Create a function that can be attached to a ModelAdmin to use as a list_display field, e.g:
    client__name = get_related_field('client__name', short_description='Client')
    """
    as_link = name.startswith(link_to_prefix)
    if as_link:
        name = name[len(link_to_prefix):]
    related_names = name.split('__')

    def getter(self, obj):
        for related_name in related_names:
            if not obj:
                continue
            obj = getattr(obj, related_name)
        if obj and as_link:
            obj = mark_safe(u'<a href="%s" class="link-with-icon">%s<i class="fa fa-caret-right"></i></a>' % \
                            (get_admin_url(obj, admin_prefix, current_app=self.admin_site.name), obj))
        return obj

    getter.admin_order_field = admin_order_field or name
    getter.short_description = short_description or related_names[-1].title().replace('_', ' ')
    if as_link:
        getter.allow_tags = True
    return getter


class RelatedFieldAdminMetaclass(type(admin.ModelAdmin)):
    related_field_admin_prefix = 'admin'

    def __new__(cls, name, bases, attrs):
        new_class = super(RelatedFieldAdminMetaclass, cls).__new__(cls, name, bases, attrs)

        for field in new_class.list_display:
            if '__' in field or field.startswith(link_to_prefix):
                if not hasattr(new_class, field):
                    setattr(new_class, field, get_related_field(
                        field, admin_prefix=cls.related_field_admin_prefix))

        return new_class


class RelatedFieldAdmin(admin.ModelAdmin):
    """
    Version of ModelAdmin that can use linked and related fields in list_display, e.g.:
    list_display = ('link_to_user', 'address__city', 'link_to_address__city', 'address__country__country_code')
    """
    __metaclass__ = RelatedFieldAdminMetaclass

    def get_queryset(self, request):
        qs = super(RelatedFieldAdmin, self).get_queryset(request)

        # Include all related fields in queryset
        select_related = []
        for field in self.list_display:
            if '__' in field:
                if field.startswith(link_to_prefix):
                    field = field[len(link_to_prefix):]
                select_related.append(field.rsplit('__', 1)[0])

        # Include all foreign key fields in queryset.
        # This is based on ChangeList.get_query_set().
        # We have to duplicate it here because select_related() only works once.
        # Can't just use list_select_related because we might have multiple__depth__fields it won't follow.
        model = qs.model
        for field_name in self.list_display:
            try:
                field = model._meta.get_field(field_name)
            except models.FieldDoesNotExist:
                continue

            if isinstance(field.remote_field, models.ManyToOneRel):
                select_related.append(field_name)

        return qs.select_related(*select_related)
