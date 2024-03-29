from django.contrib import admin
from . models import *
from . models import VendorProfile
# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(VendorProfile)
