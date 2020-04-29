from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from . import fcm as fcm_


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class FCMDeviceManager(models.Manager):
    def get_queryset(self):
        return FCMDeviceQuerySet(self.model)


class FCMDeviceQuerySet(models.query.QuerySet):
    def send_message(self, data):
        if self:
            reg_ids = list(
                self.filter(is_active=True).values_list('reg_id', flat=True))
            fcm = fcm_.FCMMessage()
            resp = fcm.send(reg_ids, **data)
            return resp


class Device(BaseModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    device_id = models.CharField(verbose_name=_("Device IMEI"),
                                 max_length=50)
    reg_id = models.CharField(verbose_name=_("GCM Registration id"),
                              max_length=255)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    objects = FCMDeviceManager()

    def __str__(self):
        return self.device_id

    class Meta:
        unique_together = ['user', 'device_id']

    def send_message(self, data):
        if self.is_active:
            fcm = fcm_.FCMMessage()
            resp = fcm.send(str(self.reg_id), **data)
            return resp
        return 'Device is Not active'
