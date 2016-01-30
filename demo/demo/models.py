from django.db import models


class Continent(models.Model):
    name = models.CharField(max_length=256)
    order = models.PositiveIntegerField()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Country(models.Model):
    continent = models.ForeignKey(Continent, null=True)
    name = models.CharField(max_length=256)
    code = models.CharField(max_length=2,
                            help_text='ISO 3166-1 alpha-2 - two character country code')
    independence_day = models.DateField(blank=True, null=True)
    area = models.BigIntegerField(blank=True, null=True)
    population = models.BigIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, help_text='Try and enter few some more lines')
    architecture = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Countries'
