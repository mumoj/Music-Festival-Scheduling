# Generated by Django 3.1.6 on 2021-04-07 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('performances', '0002_auto_20210407_0934'),
        ('accounts', '0004_auto_20210329_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='independentperformerprofile',
            name='institution',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='performances.institution'),
        ),
        migrations.AlterField(
            model_name='independentperformerprofile',
            name='performance_class',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='performances.class'),
        ),
    ]
