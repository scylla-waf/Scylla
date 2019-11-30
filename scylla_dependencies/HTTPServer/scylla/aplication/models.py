from django.db import models
from django import forms


# Create your models here.

class Request(models.Model):
    ip = models.CharField(max_length=100, blank=True, null=True)
    petition = models.CharField(max_length=100, blank=True, null=True)
    detection = models.CharField(max_length=100, blank=True, null=True)
    type_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.ip

class Variable(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    choices= [
    ('string', 'string'),
    ('numeric', 'numeric'),
    ('strange', 'strange'),
    ]
    type_variable = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple,choices=choices,)

    def __str__(self):
        return self.name
