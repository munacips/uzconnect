from django.urls import path
from  . import views
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.home,name="home"),
    url(r'polldetails/(?P<id>\d+)/$',views.polldetails,name="polldetails"),
    url(r'vote/(?P<id>\d+)/$',views.vote,name="vote")
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL , document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)