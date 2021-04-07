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
    name = models.CharField(max_length=100, null=False)
    head_of_institution = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    institution_type = models.CharField(
        choices=CHOICES,
        max_length=50
    )
    zone = models.CharField(max_length=50)
    sub_county = models.CharField(max_length=50)
    county = models.CharField(max_length=50)
    region = models.CharField(max_length=50)


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
    """Defines how a performance is involved once a performer has been registered"""
    performer = models.OneToOneField
    zonal_marks = models.IntegerField(null=True)
    sub_county_marks = models.IntegerField(null=True)
    county_marks = models.IntegerField(null=True)
    regional_marks = models.IntegerField(null=True)
    national_marks = models.IntegerField(null=True)


