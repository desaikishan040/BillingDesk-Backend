from django.contrib import admin
from .models import Company, Invoice
from django.contrib.admin import AdminSite

# class MyAdminSite(AdminSite):
#     # Text to put at the end of each page's <title>.
#     site_title = 'My site admin'
#
# admin_site = MyAdminSite()
admin.site.site_header = 'Billing desk'

# Register your models here.
admin.site.register(Company)
admin.site.register(Invoice)
