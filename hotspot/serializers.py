from django import forms
from .models import HotspotProfile, HotspotUser, RouterDevice, Voucher


class RouterForm(forms.ModelForm):
    class Meta:
        model = RouterDevice
        fields = ['name', 'host', 'port', 'username', 'password', 'use_ssl', 'is_active']
        widgets = {'password': forms.PasswordInput(render_value=True)}


class HotspotProfileForm(forms.ModelForm):
    class Meta:
        model = HotspotProfile
        fields = ['router', 'name', 'rate_limit', 'session_timeout', 'idle_timeout']


class HotspotUserForm(forms.ModelForm):
    class Meta:
        model = HotspotUser
        fields = ['router', 'username', 'password', 'profile', 'server', 'comment', 'disabled']
        widgets = {'password': forms.PasswordInput(render_value=True)}


class VoucherForm(forms.ModelForm):
    class Meta:
        model = Voucher
        fields = ['router', 'code', 'profile', 'valid_days', 'status', 'expires_at']
        widgets = {'expires_at': forms.DateTimeInput(attrs={'type': 'datetime-local'})}
