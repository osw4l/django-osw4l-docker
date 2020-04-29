from django.contrib.gis.db import models

from apps.utils.managers import Osw4lModelModelManager


class Osw4lModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    objects = Osw4lModelModelManager()

    class Meta:
        abstract = True


class Osw4lNameModel(Osw4lModel):
    name = models.CharField(
        max_length=50,
        unique=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


