from django.db import models
from config import settings


# Create your models here.
class Locality(models.Model):
    """A geographical locality within which schools compete."""
    zone = models.CharField(max_length=20)
    sub_county = models.CharField(max_length=20)
    county = models.CharField(max_length=20)
    region = models.CharField(max_length=20)
    country = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'locality'
        verbose_name_plural = 'localities'

    def __str__(self):
        return self.zone


class Institution(models.Model):
    """Defines an Institution participating in the Festival."""
    CHOICES = (
        ('NURSERY_SCHOOL', 'Nursery School'),
        ('PRIMARY_SCHOOL', 'Primary School'),
        ('SECONDARY_SCHOOL', 'Secondary School'),
        ('UNIVERSITY', 'University'),
        ('COLLAGE', 'Collage'),
        ('OTHERS', 'Others'))

    name = models.CharField(max_length=100, blank=False)
    head_of_institution = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='institution_head')
    institution_type = models.CharField(
        choices=CHOICES,
        max_length=50)
    locality = models.ForeignKey(Locality, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.name


class Class(models.Model):
    """Defines  a performance category allowed in the Festival."""
    CHOICES = (
        ('PRELIMINARY_LEVEL', 'Preliminary Level'),
        ('DIRECT_ENTRY', 'Direct Entry'))

    class_code = models.CharField(max_length=10, primary_key=True)
    class_name = models.CharField(max_length=250)
    performance_duration = models.IntegerField()
    entry_level = models.CharField(
        choices=CHOICES,
        default='PRELIMINARY_LEVEL',
        max_length=50)

    class Meta:
        verbose_name = 'class'
        verbose_name_plural = 'classes'

    def __str__(self):
        return self.class_code


class Performance(models.Model):
    """
    Defines a performance group/individual in the festival.
    """
    PERFORMANCE_TYPES = (
        ('INDEPENDENT', 'Independent'),
        ('DEPENDENT', 'Dependent'))

    GROUP_SIZES = None

    performer_name = models.CharField(max_length=50, null=True)
    performance_type = models.CharField(
        choices=PERFORMANCE_TYPES,
        max_length=15)
    performance_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    group_leader = models.ForeignKey(
        help_text="The group leader can be a teacher in charge of a dependent performance "
                  "or an independent performer leading  an independent performance.",
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='performance_group_leader')
    members = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL,
        related_name='performance_group_members')
    group_size = models.CharField(
        choices=GROUP_SIZES,
        max_length=10)
    sponsor = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='performance_sponsor',
        null=True)
    institution = models.OneToOneField(Institution, on_delete=models.CASCADE)

    zonal_marks = models.IntegerField(null=True)
    sub_county_marks = models.IntegerField(null=True)
    county_marks = models.IntegerField(null=True)
    regional_marks = models.IntegerField(null=True)
    national_marks = models.IntegerField(null=True)

    def get_performance_name(self):
        name = '%s %s ' % (self.performance_class, self.institution)
        return name.strip()

    def __str__(self):
        self.get_performance_name()


class Event(models.Model):
    """Define an event in the festival."""
    EVENT_LEVELS = (
        ('ZONAL', 'Zonal'),
        ('SUB-COUNTY', 'Sub-County'),
        ('COUNTY', 'County'),
        ('REGIONAL', 'Regional'),
        ('NATIONAL', 'National'),
    )
    venue = models.CharField(max_length=50)
    locality = models.ForeignKey(Locality, on_delete=models.DO_NOTHING, null=True)
    start_date = models.DateField()
    event_level = models.CharField(
        choices=EVENT_LEVELS,
        max_length=15)

    def __str__(self):
        return self.venue


class Theater(models.Model):
    """Define the theatres in an event"""
    name = models.CharField(max_length=15)
    venue = models.ForeignKey(Event, on_delete=models.CASCADE)
    available = models.BooleanField()
    capacity = models.IntegerField()

    def __str__(self):
        return self.name
