from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Poll(models.Model):
    title = models.CharField(max_length=100)
    end_date = models.DateTimeField()

    def __str__(self):
        return self.title


class PollNominee(models.Model):
    entry = models.CharField(max_length=200)
    poll = models.ForeignKey(Poll,on_delete=models.CASCADE)

    def __str__(self):
        return self.entry + " on " + self.poll.title

    def getPoll(self):
        return self.poll


class Vote(models.Model):
    voter = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    poll = models.ForeignKey(Poll,on_delete=models.CASCADE,unique=True)
    nominee = models.ForeignKey(PollNominee,on_delete=models.CASCADE,unique=True)