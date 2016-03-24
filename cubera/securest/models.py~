from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator #For phone number validation
from random import randint
import datetime

class Address(models.Model):
    id = models.AutoField(primary_key=True)
    TYPE_CHOICES = (
      ('customer', 'customer'),
      ('merchant', 'merchant'),
    )
    type = models.CharField(choices=TYPE_CHOICES, max_length=10)
    building_number = models.CharField(max_length=50, blank=True, null=True)
    street = models.CharField(max_length=100, blank=True, null=True)
    locality = models.CharField(max_length=50, blank=True, null=True)
    landmark = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    zipcode = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    google_maps_place_id = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'address'
    def __unicode__(self):
        return_string = (str(self.building_number) if self.building_number != None else '') + ' ' + \
            (str(self.street) if self.street != None else '') + ' ' + (str(self.locality) if self.locality != None else '')
        return unicode(return_string)


class Customers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #cust_id = models.IntegerField(unique=True)
    address = models.ForeignKey(Address, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    contact = models.CharField(validators=[phone_regex], max_length=50, blank=True, null=True, unique=True) # validators should be a list
    pocket_account_number = models.BigIntegerField(blank=True, null=True)
    pocket_account_balance = models.FloatField(blank=True, null=True)
    auth_data = models.CharField(max_length=50, blank=True, null=True)
    
    class Meta:
        managed = True
        db_table = 'customers'
    def __unicode__(self):
        return unicode(self.user)
   
class Merchants(models.Model):
    id = models.AutoField(primary_key=True)
    merchant_id = models.CharField(max_length=50, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    contact = models.CharField(validators=[phone_regex], max_length=50, blank=True, null=True, unique=True) # validators should be a list
    shop_address = models.ForeignKey(Address, blank=True, null=True)
    shop_name = models.CharField(max_length=50, blank=True, null=True)
    contact2 = models.CharField(validators=[phone_regex], max_length=50, blank=True, null=True) # validators should be a list
    contact3 = models.CharField(validators=[phone_regex], max_length=50, blank=True, null=True) # validators should be a list
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    access_token = models.CharField(max_length=50, blank=True, null=True)
    device_ip_address = models.GenericIPAddressField(blank=True, null=True)
    OS_CHOICES = (
      ('ios', 'ios'),
      ('android', 'android'),
    )
    os = models.CharField(choices=OS_CHOICES, max_length=50, blank=True, null=True)
    balance = models.FloatField(blank=True, null=True)
    
    class Meta:
        managed = True
        db_table = 'merchants'
    def __unicode__(self):
        return unicode(self.user)
     
class TransactionRequests(models.Model):
    id = models.AutoField(primary_key=True)
    transaction_id = models.CharField(max_length=20, blank=True, null=True)
    customer = models.ForeignKey(Customers, blank=True, null=True)
    nearby_merchant = models.ForeignKey(Merchants, blank=True, null=True)
    accepted_by_merchant = models.NullBooleanField()
    selected_by_customer = models.NullBooleanField()
    created_timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified_timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    distance = models.FloatField(blank=True, null=True)
    amount = models.FloatField(default=0.0, null=True)
    credited_to_merchant = models.NullBooleanField()
    debited_from_customer = models.NullBooleanField()
    
    class Meta: 
        managed = True
        db_table = 'transaction_requests'
    def __unicode__(self):
        return unicode(self.customer)
        
class OTPHistory(models.Model):
    id = models.AutoField(primary_key=True)
    #user = models.ForeignKey(User, blank=True, null=True)
    otp = models.IntegerField(default=randint(100000, 999999), blank=True, null=True)
    valid = models.NullBooleanField(default=True)
    #used_timestamp = models.DateTimeField(blank=True, null=True)
    valid_till_timestamp = models.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(days=1),blank=True, null=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    transaction_req = models.ForeignKey(TransactionRequests, blank=True, null=True)
    
    class Meta:
        managed = True
        db_table = 'otp_history'
    def __unicode__(self):
        return unicode(self.id)        

class Reviews(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, blank=True, null=True)
    transaction_req = models.ForeignKey(TransactionRequests, blank=True, null=True)
    merchant = models.ForeignKey(Merchants, blank=True, null=True)
    STAR_CHOICES = (
      (1, 1),
      (2, 2),
      (3, 3),
      (4, 4),
      (5, 5)
    )
    star_rating = models.IntegerField(choices=STAR_CHOICES, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    detailed_review = models.CharField(max_length=1000, blank=True, null=True)
    TYPE_CHOICES = (
      ('yes', 'yes'),
      ('no', 'no'),
      ('maybe', 'maybe'),
    )
    recommended = models.CharField(choices=TYPE_CHOICES, max_length=10, blank=True, null=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified_timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta: 
        managed = True
        db_table = 'reviews'
    def __unicode__(self):
        return unicode(self.user)
        

#class Transaction(models.Model):
   
