from django.db import models
from django.contrib import admin


def test_app_label():
    """
    Since Django 1.7 app_label while running tests is "suit"
    instead of "tests" in Django < 1.7
    """
    try:
        return Book._meta.app_label
    except:
        return 'tests'


class Book(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('-id',)


class Album(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name


class BookAdmin(admin.ModelAdmin):
    list_filter = ('id', 'name',)
    list_display = ('id', 'name',)

    def suit_row_attributes(self, obj, request):
        return {'class': 'suit_row_attr_class-%s' % obj.name,
                'data': obj.pk,
                'data-request': request}

    def suit_cell_attributes(self, obj, column):
        return {'class': 'suit_cell_attr_class-%s-%s' % (column, obj.name),
                'data': obj.pk}


class AlbumAdmin(admin.ModelAdmin):
    def suit_row_attributes(self, obj):
        """No request defined to test backward-compatibility"""
        return {'class': 'suit_row_album_attr_class-%s' % obj.name,
                'data-album': obj.pk}


class User(models.Model):
    """
    Class to test menu marking as active if two apps have model with same name
    """
    name = models.CharField(max_length=64)


admin.site.register(Book, BookAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(User)
