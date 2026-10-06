from django.db import models


class RouterDevice(models.Model):
    name = models.CharField(max_length=100)
    host = models.CharField(max_length=255)
    port = models.IntegerField(default=8728)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    use_ssl = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class HotspotUser(models.Model):
    router = models.ForeignKey("RouterDevice", on_delete=models.CASCADE, related_name="users")
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    profile = models.CharField(max_length=100, default="default")
    server = models.CharField(max_length=100, default="all")
    comment = models.CharField(max_length=255, blank=True)
    disabled = models.BooleanField(default=False)
    last_seen = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("router", "username")

    def __str__(self):
        return f"{self.username}@{self.router.name}"


class Voucher(models.Model):
    code = models.CharField(max_length=100, unique=True)
    profile = models.CharField(max_length=100, default="default")
    valid_days = models.IntegerField(default=7)
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.code
