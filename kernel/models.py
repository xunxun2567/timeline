__author__ = 'konglingkai'

from django.db import models
import datetime
from django.utils import timezone

class Object(models.Model):
    time = models.DateTimeField()
    branch = models.CharField(max_length=100)
    title = models.CharField(max_length=500)
    url = models.URLField(null=True, blank=True, max_length=1000)
    added_time=models.DateTimeField()

    def dump(self):
        print '%s: %s - %s' % (self.time.strftime('%Y-%m-%d'), self.title, self.url)
        for attribute in Attribute.objects.filter(object=self):
            print '    %s: %s' % (attribute.name, attribute.value)

    def is_added_today(self):
        return self.added_time>=timezone.now()-datetime.timedelta(days=1)
    is_added_today.admin_order_field='added_time'
    is_added_today.boolean=True
    is_added_today.short_description='Added today?'

class Attribute(models.Model):
    object = models.ForeignKey(Object)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=1500)
