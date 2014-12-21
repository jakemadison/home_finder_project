from django.conf.urls import patterns, url
from datagetter import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^mobile$', views.mobile_index, name='mobile'),
                       url(r'^new$', views.new_index, name='new'),)
