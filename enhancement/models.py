import openai

from django.db import models

from beelearn.models import TimestampMixin

from account.models import User


from catalogue.models import Topic


class Enhancement(TimestampMixin):
    """
    Store AI Enhanced History
    """

    class EnhancementType(models.TextChoices):
        ENHANCE = "ENHANCE", "Enhance"
        SUMMARIZE = "SUMMARIZE", "Summaize"

    type = models.TextField(choices=EnhancementType.choices)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
    )
    content = models.TextField()

    def __str__(self):
        return self.topic.title

    @staticmethod
    def enhance_topic(user: User, topic: Topic, type: EnhancementType):
        match type:
            case Enhancement.EnhancementType.ENHANCE:
                prompt = f"Explain the course topic '{topic.title}'."
                response = openai.Completion.create(
                    engine="gpt-3.5-turbo",
                    prompt=prompt,
                    stop="\n",
                )
            case Enhancement.EnhancementType.SUMMARIZE:
                prompt = (
                    f"Summarize this course {topic.title} content '{topic.content}'."
                )
                response = openai.Completion.create(
                    engine="text-davinci-002",
                    prompt=prompt,
                    temperature=0.7,
                    max_tokens=150,
                )
        content = response["choices"][0]["text"].strip()

        return Enhancement.objects.create(
            user=user,
            topic=topic,
            content=content,
        )
