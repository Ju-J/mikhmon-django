from django.contrib import admin
from .models import RouterDevice, HotspotUser, Voucher

admin.site.register(RouterDevice)
admin.site.register(HotspotUser)
admin.site.register(Voucher)
