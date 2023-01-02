from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class PostCount(models.Model):
    id = models.IntegerField(primary_key=True)
    like = models.PositiveIntegerField(default=0)
    dislike =models.PositiveIntegerField(default=0)


class PostLikeBy(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    like = models.PositiveIntegerField(default=0)
    dislike = models.PositiveIntegerField(default=0)

