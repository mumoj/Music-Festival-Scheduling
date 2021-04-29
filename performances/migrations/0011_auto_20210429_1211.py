# Generated by Django 3.1.6 on 2021-04-29 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('performances', '0010_class_performance_duration'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('venue', models.CharField(max_length=50)),
                ('event_level', models.CharField(choices=[('ZONAL', 'Zonal'), ('SUB-COUNTY', 'Sub-County'), ('COUNTY', 'County'), ('REGIONAL', 'Regional'), ('NATIONAL', 'National')], max_length=15)),
            ],
        ),
        migrations.AddField(
            model_name='performance',
            name='performance_class',
            field=models.ForeignKey(default='H001', on_delete=django.db.models.deletion.CASCADE, to='performances.class'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Theater',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capacity', models.IntegerField()),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='performances.event')),
            ],
        ),
    ]
