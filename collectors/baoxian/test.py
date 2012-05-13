__author__ = 'konglingkai'

from kernel import collector
from datetime import datetime

class TestCollector(collector.Collector):
    def fetch(self):
        collector.object_found.send(self,time=datetime.now(),title='test',url='http://dddd23233', check=False, coco='111')