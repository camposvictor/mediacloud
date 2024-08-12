# Generated by Django 5.0.4 on 2024-08-12 00:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0007_videofile_thumbnail_file"),
    ]

    operations = [
        migrations.AddField(
            model_name="audiofile",
            name="name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="imagefile",
            name="name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="videofile",
            name="name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
