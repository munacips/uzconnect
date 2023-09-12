from xml.etree.ElementTree import PI
from django.contrib import admin
from .models import Service, Good, Picture, GoodPicture

# Register your models here.
admin.site.register(Service)
admin.site.register(Good)
admin.site.register(Picture)
admin.site.register(GoodPicture)