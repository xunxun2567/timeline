from django.db import models

class Object(models.Model):
    time = models.DateTimeField()
    branch = models.CharField(max_length=100)
    title = models.CharField(max_length=500)
    url = models.URLField(null=True, blank=True)

class Attribute(models.Model):
    obj = models.ForeignKey(Object)
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

class Branch(models.Model):
    name = models.CharField(max_length=20)
    test = models.CharField(max_length=10)