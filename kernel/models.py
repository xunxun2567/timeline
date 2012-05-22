__author__ = 'konglingkai'

from django.db import models

class Object(models.Model):
    time = models.DateTimeField()
    title = models.CharField(max_length=50)
    url = models.URLField()
    branch = models.CharField(max_length=50)
    def dump(self):
        print '%s: %s - %s' % (self.time.strftime('%Y-%m-%d'), self.title, self.url)
        for attribute in Attribute.objects.filter(object=self):
            print '    %s: %s' % (attribute.name, attribute.value)

class Attribute(models.Model):
    object = models.ForeignKey(Object)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=1500)