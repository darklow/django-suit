from django.db import models

TYPE_CHOICES = ((1, 'Awesome'), (2, 'Good'), (3, 'Normal'), (4, 'Bad'))
TYPE_CHOICES2 = ((1, 'Hot'), (2, 'Normal'), (3, 'Cold'))
TYPE_CHOICES3 = ((1, 'Tall'), (2, 'Normal'), (3, 'Short'))


class Continent(models.Model):
    name = models.CharField(max_length=256)
    order = models.PositiveIntegerField()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Country(models.Model):
    continent = models.ForeignKey(Continent, null=True, on_delete=models.CASCADE)
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


class City(models.Model):
    name = models.CharField(max_length=64)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    is_capital = models.BooleanField()
    area = models.BigIntegerField(blank=True, null=True)
    population = models.BigIntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Cities (django-select2)"
        unique_together = ('name', 'country')


class Showcase(models.Model):
    name = models.CharField(max_length=64)
    help_text = models.CharField(max_length=64,
                                 help_text="Enter fully qualified name")
    multiple_in_row = models.CharField(max_length=64,
                                       help_text='Help text for multiple')
    textfield = models.TextField(blank=True,
                                 verbose_name='Autosized textfield',
                                 help_text='Try and enter few some more lines')
    readonly_field = models.CharField(max_length=127, default='Some value here')
    multiple2 = models.CharField(max_length=10, blank=True)
    date = models.DateField(blank=True, null=True)
    date_and_time = models.DateTimeField(blank=True, null=True)
    time_only = models.TimeField(blank=True, null=True, verbose_name='Time')

    date_widget = models.DateField(blank=True, null=True)
    datetime_widget = models.DateTimeField(blank=True, null=True)
    collapsed_param = models.BooleanField(default=False)

    TYPE_CHOICES = ((1, 'Awesome'), (2, 'Good'), (3, 'Normal'), (4, 'Bad'))
    TYPE_CHOICES2 = ((1, 'Hot'), (2, 'Normal'), (3, 'Cold'))
    TYPE_CHOICES3 = ((1, 'Tall'), (2, 'Normal'), (3, 'Short'))
    boolean = models.BooleanField(default=True)
    boolean_with_help = models.BooleanField(default=False, help_text="Boolean field with help text")
    horizontal_choices = models.SmallIntegerField(
        choices=TYPE_CHOICES, default=1, help_text='Horizontal choices look like this')
    vertical_choices = models.SmallIntegerField(
        choices=TYPE_CHOICES2, default=2, help_text="Some help on vertical choices")
    choices = models.SmallIntegerField(
        choices=TYPE_CHOICES3, default=3, help_text="Help text")

    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.SET_NULL)
    country2 = models.ForeignKey(Country, null=True, blank=True, related_name='showcase_country2_set', verbose_name='Django Select 2', on_delete=models.SET_NULL)
    raw_id_field = models.ForeignKey(Country, null=True, blank=True, related_name='showcase_raw_set', on_delete=models.SET_NULL)
    # linked_foreign_key = models.ForeignKey(Country, limit_choices_to={
    #     'continent__name': 'Europe'}, related_name='foreign_key_linked')
    html5_color = models.CharField(null=True, blank=True, max_length=7)
    html5_number = models.IntegerField(null=True, blank=True)
    html5_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Showcase'


# Tabular inline model for Showcase
class Movie(models.Model):
    showcase = models.ForeignKey(Showcase, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    rating = models.SmallIntegerField(choices=TYPE_CHOICES, default=2)
    description = models.TextField(blank=True)
    is_released = models.BooleanField(default=False)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ('order',)

    def __unicode__(self):
        return self.title


# Stacked inline model for Showcase
class Book(models.Model):
    showcase = models.ForeignKey(Showcase, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    rating = models.SmallIntegerField(choices=TYPE_CHOICES, help_text='Choose wisely')
    is_released = models.BooleanField(default=False)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ('order',)

    def __unicode__(self):
        return self.title


# class LargeFilterHorizontal(models.Model):
#     title = models.CharField(max_length=64)
#
#     TYPE_CHOICES= ((1, 'Awesome'), (2, 'Good'), (3, 'Normal'), (4, 'Bad'))
#     TYPE_CHOICES2 = ((1, 'Hot'), (2, 'Normal'), (3, 'Cold'))
#     TYPE_CHOICES3 = ((1, 'Tall'), (2, 'Normal'), (3, 'Short'))
#     TYPE_CHOICES4 = ((1, 'Black'), (2, 'Purple'), (3, 'Pink'))
#     TYPE_CHOICES5 = ((1, 'Image'), (2, 'Video'), (3, 'Sound'))
#     TYPE_CHOICES6 = ((1, 'Square'), (2, 'Circle'), (3, 'Triangle'))
#     TYPE_CHOICES7 = ((1, 'GIF'), (2, 'JPG'), (3, 'PNG'))
#     TYPE_CHOICES8 = ((1, 'Color'), (2, 'B&W'), (3, 'Others'))
#     horizontal_choices1 = models.SmallIntegerField(
#         choices=TYPE_CHOICES, default=1, help_text='Horizontal1 choices look like this')
#     horizontal_choices2 = models.SmallIntegerField(
#         choices=TYPE_CHOICES2, default=2, help_text="Horizontal2 choices look like this")
#     horizontal_choices3 = models.SmallIntegerField(
#         choices=TYPE_CHOICES3, default=3, help_text="Horizontal3 choices look like this")
#     horizontal_choices4 = models.SmallIntegerField(
#         choices=TYPE_CHOICES4, default=1, help_text='Horizontal4 choices look like this')
#     horizontal_choices5 = models.SmallIntegerField(
#         choices=TYPE_CHOICES5, default=2, help_text="Horizontal5 choices look like this")
#     horizontal_choices6 = models.SmallIntegerField(
#         choices=TYPE_CHOICES6, default=3, help_text="Horizontal6 choices look like this")
#     horizontal_choices7 = models.SmallIntegerField(
#         choices=TYPE_CHOICES7, default=2, help_text="Horizontal7 choices look like this")
#     horizontal_choices8 = models.SmallIntegerField(
#         choices=TYPE_CHOICES8, default=3, help_text="Horizontal8 choices look like this")
#
#     class Meta:
#         verbose_name = 'Large Filter Horizontal choice'
#         verbose_name_plural = 'Large Filter Horizontal choices'
#
#     def __unicode__(self):
#         return self.title
