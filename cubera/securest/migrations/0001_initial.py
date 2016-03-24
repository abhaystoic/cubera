# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('type', models.CharField(max_length=10, choices=[('customer', 'customer'), ('merchant', 'merchant')])),
                ('building_number', models.CharField(max_length=50, null=True, blank=True)),
                ('street', models.CharField(max_length=100, null=True, blank=True)),
                ('locality', models.CharField(max_length=50, null=True, blank=True)),
                ('landmark', models.CharField(max_length=50, null=True, blank=True)),
                ('city', models.CharField(max_length=50, null=True, blank=True)),
                ('state', models.CharField(max_length=50, null=True, blank=True)),
                ('country', models.CharField(max_length=50, null=True, blank=True)),
                ('zipcode', models.CharField(max_length=50, null=True, blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('google_maps_place_id', models.CharField(max_length=50, null=True, blank=True)),
            ],
            options={
                'db_table': 'address',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=50, null=True, blank=True)),
                ('middle_name', models.CharField(max_length=100, null=True, blank=True)),
                ('last_name', models.CharField(max_length=50, null=True, blank=True)),
                ('email', models.EmailField(max_length=100, null=True, blank=True)),
                ('contact', models.CharField(blank=True, max_length=50, unique=True, null=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])),
                ('pocket_account_number', models.BigIntegerField(null=True, blank=True)),
                ('pocket_account_balance', models.FloatField(null=True, blank=True)),
                ('auth_data', models.CharField(max_length=50, null=True, blank=True)),
                ('address', models.ForeignKey(blank=True, to='securest.Address', null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'customers',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Merchants',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('merchant_id', models.CharField(max_length=50, null=True, blank=True)),
                ('shop_name', models.CharField(max_length=50, null=True, blank=True)),
                ('contact1', models.CharField(blank=True, max_length=50, null=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])),
                ('contact2', models.CharField(blank=True, max_length=50, null=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])),
                ('contact3', models.CharField(blank=True, max_length=50, null=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])),
                ('latitude', models.DecimalField(null=True, max_digits=9, decimal_places=6, blank=True)),
                ('longitude', models.DecimalField(null=True, max_digits=9, decimal_places=6, blank=True)),
                ('access_token', models.CharField(max_length=50, null=True, blank=True)),
                ('device_ip_address', models.GenericIPAddressField(null=True, blank=True)),
                ('os', models.CharField(blank=True, max_length=50, null=True, choices=[('ios', 'ios'), ('android', 'android')])),
                ('shop_address', models.ForeignKey(blank=True, to='securest.Address', null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'merchants',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='OTPHistory',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('otp', models.IntegerField(default=165482, null=True, blank=True)),
                ('valid', models.NullBooleanField(default=True)),
                ('valid_till_timestamp', models.DateTimeField(default=datetime.datetime(2016, 3, 23, 18, 44, 9, 116242), null=True, blank=True)),
                ('created_timestamp', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'db_table': 'otp_history',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('star_rating', models.IntegerField(blank=True, null=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=200, null=True, blank=True)),
                ('detailed_review', models.CharField(max_length=1000, null=True, blank=True)),
                ('recommended', models.CharField(blank=True, max_length=10, null=True, choices=[('yes', 'yes'), ('no', 'no'), ('maybe', 'maybe')])),
                ('created_timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified_timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('merchant', models.ForeignKey(blank=True, to='securest.Merchants', null=True)),
            ],
            options={
                'db_table': 'reviews',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TransactionRequests',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('transaction_id', models.CharField(max_length=20, null=True, blank=True)),
                ('accepted_by_merchant', models.NullBooleanField()),
                ('selected_by_customer', models.NullBooleanField()),
                ('created_timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified_timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('customer', models.ForeignKey(blank=True, to='securest.Customers', null=True)),
                ('nearby_merchant', models.ForeignKey(blank=True, to='securest.Merchants', null=True)),
            ],
            options={
                'db_table': 'transaction_requests',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='reviews',
            name='transaction_req',
            field=models.ForeignKey(blank=True, to='securest.TransactionRequests', null=True),
        ),
        migrations.AddField(
            model_name='reviews',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='otphistory',
            name='transaction_req',
            field=models.ForeignKey(blank=True, to='securest.TransactionRequests', null=True),
        ),
    ]
