# Generated by Django 2.2.13 on 2020-11-11 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studygroups', '0140_auto_20201110_0854'),
    ]

    operations = [
        migrations.AddField(
            model_name='studygroup',
            name='online',
            field=models.BooleanField(default=False),
        ),
    ]
