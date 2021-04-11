from django.db import models


# Create your models here.
class Channel(models.Model):
    nickname = models.CharField(max_length=50, primary_key=True)
    url = models.TextField()
    transcode_pid = models.IntegerField(default=0)
    hitting_count = models.IntegerField(default=0)
