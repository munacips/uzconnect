from django.urls import path
from  . import views
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.home,name="home"),
    path('goods/',views.goods,name="bizgoods"),
    path('post/',views.post,name="post"),
    path('postservice/',views.postservice,name="postservice"),
    path('postproduct/',views.postproduct,name="postproduct"),
    url(r'gooddetails/(?P<id>\d+)/$',views.good,name="good"),
    url(r'details/(?P<id>\d+)/$',views.details,name="details"),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL , document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)