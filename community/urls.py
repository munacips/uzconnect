from django.urls import path
from  . import views
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.home,name="home"),
    path('coursemash/',views.coursemash,name="coursemash"),
    path('studentsearch/',views.studentsearch,name="studentsearch"),
    path('login/',views.log_in,name="login"),
    path('signup/',views.signup,name="signup"),
    path('logout/',views.log_out,name="logout"),
    path('myaccount/',views.account,name="myaccount"),
    path('myprofile/',views.myprofile,name="myprofile"),
    url(r'deletequote/(?P<id>\d+)/$',views.deletequote,name="deletequote"),
    url(r'deleteser/(?P<id>\d+)/$',views.deleteser,name="deleteser"),
    url(r'deletegood/(?P<id>\d+)/$',views.deletegood,name="deletegood"),
    url(r'follow/(?P<id>\d+)/$',views.follow,name="follow"),
    url(r'unfollow/(?P<id>\d+)/$',views.unfollow,name="unfollow"),
    path('add/',views.add,name="add"),
    path('addpost/',views.addpost,name="addpost"),
    path('addpics/',views.addpics,name="addpics"),
    url(r'addpicsfile/(?P<id>\d+)/$',views.addpicsfile,name="addpicsfile"),
    url(r'editser/(?P<id>\d+)/$',views.editser,name="editser"),
    url(r'editgood/(?P<id>\d+)/$',views.editgood,name="editgood"),
    path('confirm/',views.confirm,name="confirm"),
    url(r'userprofile/(?P<id>\d+)/$',views.userprofile,name="userprofile"),
    url(r'details/(?P<id>\d+)/$',views.details,name="details"),
    url(r'like/(?P<id>\d+)/$',views.like,name="like"),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL , document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)