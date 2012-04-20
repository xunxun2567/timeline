from kernel import collector

class TopicCollector(collector.Collector):
    def pull(self):
        print "pulling from topic collector!!"
        collector.object_found.send(self, title='test', url='http://www.google.com', time='2012-4-20')

