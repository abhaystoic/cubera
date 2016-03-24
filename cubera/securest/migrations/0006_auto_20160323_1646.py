# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('securest', '0005_auto_20160323_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otphistory',
            name='otp',
            field=models.IntegerField(default=605188, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='otphistory',
            name='valid_till_timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 24, 16, 46, 45, 528946), null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='transactionrequests',
            name='amount',
            field=models.FloatField(default=0.0, null=True),
        ),
    ]
