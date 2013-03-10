from django.db import models
from django.contrib import admin


class Book(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name


class Album(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name


class BookAdmin(admin.ModelAdmin):
    list_filter = ('id', 'name',)


admin.site.register(Book, BookAdmin)
admin.site.register(Album)
