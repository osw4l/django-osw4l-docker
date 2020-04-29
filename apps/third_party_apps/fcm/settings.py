from . import models
from django.conf import settings

DEVICE_MODEL = models.Device
API_URL = "https://fcm.googleapis.com/fcm/send"
API_KEY = settings.FIREBASE_CLOUD_MESSAGING_TOKEN
MAX_RECIPIENTS = 1000


def get_device_model():
    return DEVICE_MODEL
