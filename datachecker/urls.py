__author__ = 'jmadison'
from django.conf.urls import patterns, url
from datachecker import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       )
