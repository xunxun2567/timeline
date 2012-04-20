from django.db import models

class Object(models.Model):
    time = models.DateTimeField()
    branch = models.CharField(max_length=100)
    title = models.CharField(max_length=500)
    url = models.URLField()

class Branch(models.Model):
    name = models.CharField(max_length=20)
