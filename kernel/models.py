__author__ = 'konglingkai'

from django.db import models

class Object(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    url = models.URLField()
    line = models.CharField(max_length=50)

class Attribute(models.Model):
    object = models.ForeignKey(Object)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)