# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('securest', '0004_auto_20160323_1559'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='merchants',
            name='contact1',
        ),
        migrations.AddField(
            model_name='merchants',
            name='balance',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='transactionrequests',
            name='credited_to_merchant',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='transactionrequests',
            name='debited_from_customer',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='otphistory',
            name='otp',
            field=models.IntegerField(default=763876, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='otphistory',
            name='valid_till_timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 24, 16, 40, 23, 155762), null=True, blank=True),
        ),
    ]
