from django.urls import path

from atast_web import views


urlpatterns = [
    path("", views.sss, name="sss-home"),
    path("about/", views.sss, name="sss-about"),
    path("speakers/", views.sss, name="sss-speakers"),
    path("schedule/", views.sss, name="sss-schedule"),
    path("archives/", views.sss, name="sss-archives"),
    path("contact/", views.sss, name="sss-contact"),
]
