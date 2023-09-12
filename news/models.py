from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100)
    body = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    feature_pic = models.ImageField(upload_to='news/pics/')
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class PostImage(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='news/pics/')


class PostComment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    comment = models.CharField(max_length=400)
    date_posted = models.DateTimeField(auto_now_add=True)