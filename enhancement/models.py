from django.db import models

from beelearn.models import TimestampMixin

from account.models import User


from catalogue.models import Topic


class Enhancement(TimestampMixin):
    """
    Store AI Enhanced History
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.topic.title

    @staticmethod
    def enhance_topic(topic: Topic):
        return Enhancement.objects.create(topic=topic, content=None)
