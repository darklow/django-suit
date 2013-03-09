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


admin.site.register(Book)
admin.site.register(Album)
