# Generated by Django 3.1.6 on 2021-06-03 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('performances', '0017_auto_20210603_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performance',
            name='institution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='performances.institution'),
        ),
    ]