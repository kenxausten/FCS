# from peewee import *
#please refer to: http://docs.peewee-orm.com/en/latest/peewee/models.html

import os
import sys
HOME = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.extend([HOME,])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'conf.settings')

from django.db import models
from django.core.management.commands import syncdb


class Image(models.Model):

    name = models.CharField(max_length=1024)
    path = models.CharField(max_length=1024)
    token = models.CharField(max_length=1024)
    create_time = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'db'



if __name__ == '__main__':
    if len(sys.argv) > 1:
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)

    # Image.objects.create(name='test', path='test', token='test')
    #  print([i.name for i in Image.objects.all()])


