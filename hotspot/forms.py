from django import forms
from .models import HotspotUser, RouterDevice, Voucher


class RouterForm(forms.ModelForm):
    class Meta:
        model = RouterDevice
        fields = ["name", "host", "port", "username", "password", "use_ssl", "is_active"]
        widgets = {
            "password": forms.PasswordInput(render_value=True),
        }


class HotspotUserForm(forms.ModelForm):
    class Meta:
        model = HotspotUser
        fields = ["router", "username", "password", "profile", "server", "comment", "disabled"]
        widgets = {
            "password": forms.PasswordInput(render_value=True),
        }


class VoucherForm(forms.ModelForm):
    class Meta:
        model = Voucher
        fields = ["code", "profile", "valid_days", "expires_at"]
