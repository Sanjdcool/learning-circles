# -*- coding: utf-8 -*-


from django.db import migrations, models
import datetime
from django.utils.timezone import utc

def set_meeting_date(apps, schema_editor):
    StudyGroupMeeting = apps.get_model('studygroups', 'StudyGroupMeeting')
    for meeting in StudyGroupMeeting.objects.all():
        meeting.meeting_date = meeting.meeting_time.date()
        meeting.save()


class Migration(migrations.Migration):

    dependencies = [
        ('studygroups', '0062_auto_20160308_1026'),
    ]

    operations = [
        migrations.AddField(
            model_name='studygroupmeeting',
            name='meeting_date',
            field=models.DateField(default=datetime.datetime(2016, 3, 9, 13, 1, 56, 898627, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.RunPython(set_meeting_date),
    ]
