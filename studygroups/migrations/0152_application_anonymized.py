# Generated by Django 2.2.13 on 2021-07-16 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studygroups', '0151_set_survey_sent_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='anonymized',
            field=models.BooleanField(default=False),
        ),
    ]