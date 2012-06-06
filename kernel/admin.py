__author__ = 'xukaifang'

from kernel.models import Object
from django.contrib import admin


class ObjectAdmin(admin.ModelAdmin):
    list_display = ('branch','title','added_time','is_added_today')
    list_filter=['added_time','branch']

    fieldsets=[
        ('Objects',{'fields':['branch']}),
        ('Details',{'fields':['title','time','added_time','url']})
        ]

admin.site.register(Object,ObjectAdmin)
