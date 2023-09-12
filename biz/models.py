from django.db import models
from sqlalchemy import null
from community.models import Account

# Create your models here.
class Service(models.Model):
    service = models.CharField(max_length=100)
    estimate_prize = models.DecimalField(max_digits=15,decimal_places=2)
    provider = models.ForeignKey(Account,on_delete=models.CASCADE)
    phone_or_whatsapp_number = models.IntegerField()
    description = models.TextField()
    feature_pic = models.ImageField(upload_to='biz/pics/')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.service + " provided by " + self.provider.user.username


class Good(models.Model):
    good = models.CharField(max_length=100)
    estimate_prize = models.DecimalField(max_digits=15,decimal_places=2)
    provider = models.ForeignKey(Account,on_delete=models.CASCADE)
    phone_or_whatsapp_number = models.IntegerField()
    description = models.TextField()
    feature_pic = models.ImageField(upload_to='biz/pics/')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.good + " sold by " + self.provider.user.username


class Picture(models.Model):
    service = models.ForeignKey(Service,on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='biz/pics/')


class GoodPicture(models.Model):
    good = models.ForeignKey(Good,on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='biz/pics/')