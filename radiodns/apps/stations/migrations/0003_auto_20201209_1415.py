# Generated by Django 3.0.7 on 2020-12-09 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stations', '0002_auto_20200617_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='station',
            name='radioepg_service',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='station',
            name='radiotag_service',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='station',
            name='radiovis_service',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]