from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='posts_id')
    title = models.CharField(max_length=200)
    text = models.TextField()
    public = models.BooleanField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Like(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author}-->{self.post}'


class Dislike(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author}-->{self.post}'


class Subscription(models.Model):
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE,
                                   related_name='subscribed_id')
    subscribed = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE,
                                   related_name='subscriber_id')

    def __str__(self):
        return f'{self.subscriber}-->{self.subscribed}'
