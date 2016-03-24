# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('securest', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otphistory',
            name='otp',
            field=models.IntegerField(default=692057, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='otphistory',
            name='valid_till_timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 23, 18, 45, 9, 310392), null=True, blank=True),
        ),
    ]
