from django.conf.urls import patterns, url
from craig_data_getter import views

urlpatterns = patterns('', url(r'^$', views.index, name='index'))
