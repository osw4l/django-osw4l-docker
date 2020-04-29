from django.db import models


class Osw4lModelModelQuerySet(models.QuerySet):
    def all(self):
        return self.filter(active=True)

    def removed(self):
        return self.filter(active=False)


class Osw4lModelModelManager(models.Manager):
    def get_queryset(self):
        return Osw4lModelModelQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all()

    def removed(self):
        return self.get_queryset().removed()

