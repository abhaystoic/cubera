# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('securest', '0002_auto_20160322_1845'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionrequests',
            name='distance',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='otphistory',
            name='otp',
            field=models.IntegerField(default=229754, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='otphistory',
            name='valid_till_timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 23, 19, 10, 43, 657798), null=True, blank=True),
        ),
    ]
