from django.contrib import admin
from .models import Device


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['name', 'device_id', 'reg_id', 'is_active', 'user']
    fields = ['name', 'device_id', 'reg_id', 'is_active', 'user']
    ordering = ['name',]

