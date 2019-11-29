from django.db import models


# Create your models here.

class Request(models.Model):
    ip = models.CharField(max_length=100, blank=True, null=True)
    petition = models.CharField(max_length=100, blank=True, null=True)
    detection = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.ip


class Variables(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    var_type = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
