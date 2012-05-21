__author__ = 'konglingkai'

from django.db import models

class Object(models.Model):
    time = models.DateTimeField()
    branch = models.CharField(max_length=100)
    title = models.CharField(max_length=500)
    url = models.URLField(null=True, blank=True, max_length=1000)

    def dump(self):
        print '%s: %s - %s' % (self.time.strftime('%Y-%m-%d'), self.title, self.url)
        for attribute in Attribute.objects.filter(object=self):
            print '    %s: %s' % (attribute.name, attribute.value)

class Attribute(models.Model):
    object = models.ForeignKey(Object)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=1500)
