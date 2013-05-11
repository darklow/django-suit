from django.db import models
from django.contrib import admin


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

    def suit_row_attributes(self, obj):
        return {'class': 'suit_row_attr_class-%s' % obj.name, 'data': obj.pk}

    def suit_cell_attributes(self, obj, column):
        return {'class': 'suit_cell_attr_class-%s-%s' % (column, obj.name),
                'data': obj.pk}


admin.site.register(Book, BookAdmin)
admin.site.register(Album)
