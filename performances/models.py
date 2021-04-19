from django.db import models
from config import settings


# Create your models here.
class Institution(models.Model):
    """Defines an Institution participating in the Festival."""
    CHOICES = (
        ('NURSERY_SCHOOL', 'Nursery School'),
        ('PRIMARY_SCHOOL', 'Primary School'),
        ('SECONDARY_SCHOOL', 'Secondary School'),
        ('UNIVERSITY', 'University'),
        ('COLLAGE', 'Collage'),
        ('OTHERS', 'Others')

    )
    name = models.CharField(max_length=100, blank=False)
    head_of_institution = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    institution_type = models.CharField(
        choices=CHOICES,
        max_length=50
    )
    zone = models.CharField(max_length=50, blank=False)
    sub_county = models.CharField(max_length=50, blank=False)
    county = models.CharField(max_length=50, blank=False)
    region = models.CharField(max_length=50, blank=False)


class Class(models.Model):
    """Defines  a performance category allowed in the Festival."""
    CHOICES = (
        ('PRELIMINARY_LEVEL', 'Preliminary Level'),
        ('DIRECT_ENTRY', 'Direct Entry')
    )
    class_code = models.CharField(max_length=10,
                                  primary_key=True)
    class_name = models.CharField(max_length=250)
    entry_level = models.CharField(
        choices=CHOICES,
        default='PRELIMINARY_LEVEL',
        max_length=50,
    )


class Performance(models.Model):
    """
    Defines a performance group/individual in the festival.
    """
    PERFORMANCE_TYPES = (
        ('INDEPENDENT', 'Independent'),
        ('DEPENDENT', 'Dependent'),
    )

    GROUP_SIZES = None

    performer_name = models.CharField(max_length=50)
    performance_type = models.CharField(
        choices=PERFORMANCE_TYPES,
        max_length=15)
    # The group leader can be a teacher in charge of a dependent performance
    # or an independent performer leading the rest of an independent performance.
    group_leader = models.ForeignKey(
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


