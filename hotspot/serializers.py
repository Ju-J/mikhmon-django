from rest_framework import serializers
from .models import HotspotUser, RouterDevice, Voucher


class RouterDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouterDevice
        fields = "__all__"


class HotspotUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotspotUser
        fields = "__all__"


class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = "__all__"
