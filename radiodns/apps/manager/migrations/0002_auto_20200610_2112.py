# Generated by Django 3.0.7 on 2020-06-10 21:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("manager", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="organization",
            name="users",
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="logoimage",
            name="organization",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="manager.Organization"
            ),
        ),
    ]