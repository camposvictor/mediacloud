# Generated by Django 5.0.4 on 2024-08-10 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_mediafile_core_mediaf_descrip_881dc0_idx_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediafile',
            name='file',
            field=models.FileField(upload_to='media/'),
        ),
    ]
