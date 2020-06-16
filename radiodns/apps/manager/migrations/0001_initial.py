# Generated by Django 3.0.7 on 2020-06-10 21:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("localization", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="LogoImage",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("file", models.ImageField(blank=True, null=True, upload_to="")),
                ("scaled32x32", models.ImageField(blank=True, null=True, upload_to="")),
                (
                    "scaled112x32",
                    models.ImageField(blank=True, null=True, upload_to=""),
                ),
                (
                    "scaled128x128",
                    models.ImageField(blank=True, null=True, upload_to=""),
                ),
                (
                    "scaled320x240",
                    models.ImageField(blank=True, null=True, upload_to=""),
                ),
                (
                    "scaled600x600",
                    models.ImageField(blank=True, null=True, upload_to=""),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Organization",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("codops", models.CharField(max_length=255)),
                ("short_name", models.CharField(max_length=8)),
                ("medium_name", models.CharField(max_length=16)),
                ("long_name", models.CharField(max_length=128)),
                ("short_description", models.CharField(max_length=180)),
                (
                    "long_description",
                    models.CharField(blank=True, max_length=1200, null=True),
                ),
                ("url_default", models.URLField()),
                (
                    "postal_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("street", models.CharField(blank=True, max_length=255, null=True)),
                ("city", models.CharField(blank=True, max_length=255, null=True)),
                ("zipcode", models.CharField(blank=True, max_length=25, null=True)),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=128, null=True),
                ),
                ("default_image_id", models.IntegerField(blank=True, null=True)),
                (
                    "default_language",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="localization.Language",
                    ),
                ),
                (
                    "location_country",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="localization.Ecc",
                    ),
                ),
            ],
        ),
    ]