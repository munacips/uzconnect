from django import forms
from django.contrib.auth.models import User

from biz.models import Good
from .models import Account, Comment, Quote
from news.models import Post, PostImage

class ProgramForm(forms.Form):
    PROGRAMS = [
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
    program = forms.ChoiceField(choices=PROGRAMS)


class SearchUserForm(forms.Form):
    name = forms.CharField()


class LoginForm(forms.Form):
    username = forms.CharField(label = 'Username', max_length = 164)
    password = forms.CharField(label = 'Password', widget=forms.PasswordInput)


class SignUpForm(forms.ModelForm):
    username = forms.CharField(label="Username")
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)



    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.exclude(pk=self.instance.pk).get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(u'Username "%s" is already in use.' % username)

    def clean_email(self):
        data = self.cleaned_data['email']
        if "@students.uz.ac.zw" not in data:
            raise forms.ValidationError("Must be a UZ email address")
        return data
    
    class Meta:
        model = Account
        fields = ['program','display_picture']
    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def __init__(self,*args,**kwargs):
        super(SignUpForm,self).__init__(*args,**kwargs)
        self.fields['display_picture'].required = True


class QuoteForm(forms.ModelForm):
    quote = forms.CharField(widget = forms.Textarea(attrs={'rows':1,'cols':80,'placeholder':'Add a quote...'}),label='')
    class Meta:
        model = Quote
        fields = ['quote']


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','body','feature_pic']


class AddPicsForms(forms.Form):
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple':True}))

class GoodForm(forms.ModelForm):
    good = forms.CharField(label='New Name')
    class Meta:
        model = Good
        fields = ['good','estimate_prize','phone_or_whatsapp_number','description','feature_pic']

    def __init__(self,*args,**kwargs):
        super(GoodForm,self).__init__(*args,**kwargs)
        self.fields['good'].required = False
        self.fields['estimate_prize'].required = False
        self.fields['phone_or_whatsapp_number'].required = False
        self.fields['description'].required = False
        self.fields['feature_pic'].required = False


class ServiceForm(forms.ModelForm):
    service = forms.CharField(label='New Name')
    class Meta:
        model = Good
        fields = ['service','estimate_prize','phone_or_whatsapp_number','description','feature_pic']

    def __init__(self,*args,**kwargs):
        super(ServiceForm,self).__init__(*args,**kwargs)
        self.fields['service'].required = False
        self.fields['estimate_prize'].required = False
        self.fields['phone_or_whatsapp_number'].required = False
        self.fields['description'].required = False
        self.fields['feature_pic'].required = False


class ConfirmEmail(forms.Form):
    integer = forms.CharField(label='Confirm Email')


class CommentForm(forms.Form):
    comment = forms.CharField(widget = forms.Textarea(attrs={'rows':1,'cols':80,'placeholder':'Add a comment...'}),label='')