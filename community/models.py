from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
    PROGRAM = [
        ('aa','HVCDAM'),
        ('ab','HDCS'),
        ('ac','HANRE'),
        ('ad','HAI'),
        ('ae','HPPST'),
        ('af','HHPS'),
        ('ag','HCISS'),
        ('ah','HLPNS'),
        ('ai','HLIGC'),
        ('aj','HRSLPE'),
        ('aj','HMDST'),
        ('ak','HSSLM'),
        ('al','HWWMS'),
        ('am','HAEMS'),
        ('an','HCSRL'),
        ('ao','HAEST'),
        ('ap','HAEDMS'),
        ('aq','HFE'),
        ('ar','HWRIE'),
        ('as','HAPPDSE'),
        ('at','HFTRP'),
        ('au','HMMP'),
        ('av','HMMC'),
        ('aw','HLLIE'),
        ('ax','HMCTI'),
        ('ay','HMHT'),
        ('az','HPEHD'),
        ('ba','HRLDS'),
        ('bb','HAHKS'),
        ('bc','HASHD'),
        ('bd','DAH'),
        ('be','HIA'),
        ('bf','BAHEH'),
        ('bg','HHWS'),
        ('bh','HCDA'),
        ('bi','HJMB'),
        ('bj','HCPST'),
        ('bk','HRRDM'),
        ('bl','HPSACCF'),
        ('bm','HFORACC'),
        ('bn','HACCN'),
        ('bo','HFCSDA'),
        ('bp','HFISMGT'),
        ('bq','HARMGT'),
        ('br','HLHM'),
        ('bs','HCAHC'),
        ('bt','HITMI'),
        ('bu','HBED'),
        ('bv','HCM'),
        ('bw','HBMSDA'),
        ('bx','HBMI'),
        ('by','HDBANK'),
        ('bz','HPRM'),
        ('ca','HSCM'),
        ('cb','HECD'),
        ('cc','HBIE'),
        ('ca','HFET'),
        ('cb','HCOE'),
        ('cc','HET'),
        ('cd','HCF'),
        ('ce','HNE'),
        ('cf','HDS'),
        ('cg','HCE'),
        ('ch','HHE'),
        ('ci','HSE'),
        ('cj','HCS'),
        ('ck','HAI'),
        ('cl','HCC'),
        ('cm','HAUD'),
        ('cn','HPM'),
        ('co','HBMLS'),
        ('cp','HPT'),
        ('cq','HOT'),
        ('cr','HOE'),
        ('cs','HNS'),
        ('ct','HEHP'),
        ('cu','HRD'),
        ('cv','HRT'),
        ('cw','BSHO'),
        ('cx','BMS-MBChB'),
        ('cy','BMS-BDS'),
        ('cz','HPST'),
        ('da','HBIOENG'),
        ('db','HMANI'),
        ('dc','HSLT'),
        ('dd','BEDHJE'),
        ('de','HJEVA'),
        ('df','HJELA'),
        ('dg','HJESS'),
        ('dh','HJEMA'),
        ('di','HDMJES'),
        ('dj','HDMES'),
        ('dk','HEDSP'),
        ('dl','BEHSNAT'),
        ('dm','BSHBC'),
        ('dn','BEHCIMP'),
        ('do','BEHLG'),
        ('dp','BEHLL'),
        ('dq','BEHCRE'),
        ('dr','BEHHHED'),
        ('ds','HEMST'),
        ('dt','HMP'),
        ('du','HPAHE'),
        ('dv','HADTE'),
        ('dw','HENCEQS'),
        ('dx','BARCH'),
        ('dy','HCE (eng)'),
        ('dz','HENCEQS (civil)'),
        ('ea','HMIE'),
        ('eb','HMTE'),
        ('ec','HMET'),
        ('ed','HENMECH'),
        ('ee','HENIND'),
        ('ef','HENMTR'),
        ('eg','HENELENG'),
        ('eh','HENPENG'),
        ('ei','AUTO'),
        ('ej','AEROV'),
        ('ek','AEROM'),
        ('el','HGEG'),
        ('em','HGES'),
        ('en','HLAM'),
        ('eo','HSPM'),
        ('ep','HTSD'),
        ('eq','HRE'),
        ('er','LLBS'),
        ('es','LLBSS'),
        ('et','HBCBMB'),
        ('eu','HBCCBT'),
        ('ev','HBCGBE'),
        ('ew','HBCBIM'),
        ('ex','HBCIEM'),
        ('ey','HBCBPBMC'),
        ('ez','BZHSC'),
        ('fa','HFRWE'),
        ('f','HBHC'),
        ('f','HPEC'),
        ('f','HASE'),
        ('f','HFSSC'),
        ('f','HICH'),
        ('f','HPHC'),
        ('f','HGL'),
        ('f','HPCT'),
        ('f','HGISEO'),
        ('f','HGISINT'),
        ('f','MCH'),
        ('f','HASC'),
        ('f','HFM'),
        ('f','HDSC'),
        ('f','HASTS'),
        ('f','HND'),
        ('f','HFST'),
        ('f','HSST'),
        ('f','HMCS'),
        ('f','HIPH'),
        ('f','HMS'),
        ('f','HMPH'),
        ('f','GPM'),
        ('f','POSD'),
        ('f','BSCID'),
        ('ga','BSTACD'),
        ('gb','HISO'),
        ('gc','HUD'),
        ('gd','HCS (crim)'),
        ('ge','BCLL'),
        ('gf','HSSM'),
        ('gg','HPSAD'),
        ('gh','HIOP'),
        ('gi','HCDP'),
        ('gj','HDP'),
        ('gk','HFPC'),
        ('gl','HTSD'),
        ('gm','HSW'),
        ('gn','HVSB'),
        ('go','HVSP'),
        ('gp','HVST'),
        ('gq','BVSc'),
    ]
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    program = models.CharField(max_length=2,choices=PROGRAM)
    display_picture = models.ImageField(upload_to='accounts/display_pictures/',null=True,blank=True)
    editor = models.BooleanField(default=False)
    activated = models.BooleanField(default=False)
    bio = models.TextField(blank=True,null=True,max_length=1000)
    followers = models.ManyToManyField(User,related_name='user_followers',symmetrical=False,blank=True)
    following = models.ManyToManyField(User,related_name='user_following',symmetrical=False,blank=True)


    def __str__(self):
        return self.user.username

    def count_followers(self):
        return self.followers.count()

    def count_following(self):
        return self.following.count()

    def get_bio(self):
        return self.bio

class Quote(models.Model):
    quoter = models.ForeignKey(User,on_delete=models.CASCADE)
    quote = models.TextField(max_length=5000)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-time']

class QuoteLike(models.Model):
    liker = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    quote = models.ForeignKey(Quote,on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-time']


class DisplayPic(models.Model):
    pic = models.ImageField(upload_to='accounts/displayPictures/',null=True,blank=True)


class Comment(models.Model):
    quote = models.ForeignKey(Quote,on_delete=models.CASCADE)
    commenter = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    comment = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-time']
