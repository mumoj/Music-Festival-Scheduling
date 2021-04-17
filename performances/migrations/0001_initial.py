# Generated by Django 3.1.6 on 2021-03-28 10:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('class_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('class_name', models.CharField(max_length=250)),
                ('entry_level', models.CharField(choices=[('PRELIMINARY_LEVEL', 'Preliminary Level'), ('DIRECT_ENTRY', 'Direct Entry')], default='PRELIMINARY_LEVEL', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zonal_marks', models.IntegerField(null=True)),
                ('sub_county_marks', models.IntegerField(null=True)),
                ('county_marks', models.IntegerField(null=True)),
                ('regional_marks', models.IntegerField(null=True)),
                ('national_marks', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('institution_type', models.CharField(choices=[('NURSERY_SCHOOL', 'Nursery School'), ('PRIMARY_SCHOOL', 'Primary School'), ('SECONDARY_SCHOOL', 'Secondary School'), ('UNIVERSITY', 'University'), ('COLLAGE', 'Collage'), ('OTHERS', 'Others')], max_length=50)),
                ('head_of_institution', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]