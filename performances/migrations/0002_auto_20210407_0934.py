# Generated by Django 3.1.6 on 2021-04-07 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('performances', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='county',
            field=models.CharField(default='Kesses', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='institution',
            name='region',
            field=models.CharField(default='Kesses', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='institution',
            name='sub_county',
            field=models.CharField(default='Uasin Gishu', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='institution',
            name='zone',
            field=models.CharField(default='Nakuru', max_length=50),
            preserve_default=False,
        ),
    ]
