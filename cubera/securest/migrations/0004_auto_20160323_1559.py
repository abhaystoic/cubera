# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('securest', '0003_auto_20160322_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchants',
            name='contact',
            field=models.CharField(blank=True, max_length=50, unique=True, null=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")]),
        ),
        migrations.AddField(
            model_name='merchants',
            name='email',
            field=models.EmailField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='merchants',
            name='first_name',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='merchants',
            name='last_name',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='merchants',
            name='middle_name',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='transactionrequests',
            name='amount',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='otphistory',
            name='otp',
            field=models.IntegerField(default=407635, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='otphistory',
            name='valid_till_timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 24, 15, 59, 45, 886052), null=True, blank=True),
        ),
    ]
