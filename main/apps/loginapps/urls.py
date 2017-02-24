from django.conf.urls import url
from . import views
# from django.contrib import

#this is your routes
urlpatterns = [
    url(r'^$', views.index),
    url(r'^success$', views.success),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout)
    ]
