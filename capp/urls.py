from os import name
from django.urls import path
from capp import views
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path("index/", views.index, name="index"),
    path("index/guest/", views.indexguest, name="indexguest"),
    path("api/run/", views.runb.as_view()),
    path("api/run/inp/", views.inprun.as_view()),
    path("login/", views.loginview, name="loginview"),
    path("register/", views.registerview, name="registerview"),
    path("api/save/", views.savefile.as_view()),
    path("showfile/<str:filename>", views.showfile,name="showfile"),
    path("allfiles/", views.allflesview, name="allfileview"),
    path("logout/", views.logoutview, name="logout"),
    path("api/checkusername/", views.checkusername.as_view()),
    path("api/deletefile/", views.deletefile.as_view())
]