from django.db import models
import uuid


class RouterDevice(models.Model):
    name = models.CharField(max_length=100, unique=True)
    host = models.CharField(max_length=255)
    port = models.IntegerField(default=8728)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    use_ssl = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_connected = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class HotspotProfile(models.Model):
    router = models.ForeignKey(RouterDevice, on_delete=models.CASCADE, related_name='profiles')
    name = models.CharField(max_length=100)
    rate_limit = models.CharField(max_length=100, default='unlimited')
    session_timeout = models.IntegerField(default=0)
    idle_timeout = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('router', 'name')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} @ {self.router.name}"


class HotspotUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    router = models.ForeignKey(RouterDevice, on_delete=models.CASCADE, related_name='hotspot_users')
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    profile = models.CharField(max_length=100, default='default')
    server = models.CharField(max_length=100, default='all')
    comment = models.CharField(max_length=255, blank=True)
    disabled = models.BooleanField(default=False)
    last_seen = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('router', 'username')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username}@{self.router.name}"


class Voucher(models.Model):
    STATUS_CHOICES = [
        ('unused', 'Unused'),
        ('used', 'Used'),
        ('expired', 'Expired'),
    ]

    code = models.CharField(max_length=100, unique=True)
    router = models.ForeignKey(RouterDevice, on_delete=models.CASCADE, related_name='vouchers', null=True, blank=True)
    profile = models.CharField(max_length=100, default='default')
    valid_days = models.IntegerField(default=7)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unused')
    used_by = models.CharField(max_length=100, null=True, blank=True)
    used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.code


class ActiveSession(models.Model):
    router = models.ForeignKey(RouterDevice, on_delete=models.CASCADE, related_name='active_sessions')
    username = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    mac_address = models.CharField(max_length=17)
    bytes_in = models.BigIntegerField(default=0)
    bytes_out = models.BigIntegerField(default=0)
    started_at = models.DateTimeField()
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('router', 'username', 'ip_address')
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.username} @ {self.router.name}"


class BandwidthLog(models.Model):
    router = models.ForeignKey(RouterDevice, on_delete=models.CASCADE, related_name='bandwidth_logs')
    username = models.CharField(max_length=100)
    bytes_in = models.BigIntegerField()
    bytes_out = models.BigIntegerField()
    session_start = models.DateTimeField()
    session_end = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-session_start']

    def __str__(self):
        return f"{self.username} - {self.bytes_in + self.bytes_out} bytes"


class AdminUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.username
