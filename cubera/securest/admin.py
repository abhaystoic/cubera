from django.contrib import admin

# Register your models here.

from securest.models import *

admin.site.register(Address)
admin.site.register(Merchants)
admin.site.register(Customers)
admin.site.register(TransactionRequests)
admin.site.register(OTPHistory)
admin.site.register(Reviews)
