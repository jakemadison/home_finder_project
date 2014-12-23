from django.conf.urls import patterns, url
from datagetter import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^mobile$', views.mobile_index, name='mobile'),
                       url(r'^new$', views.new_index, name='new'),
                       url(r'^rate_post$', views.rate_post, name='rate_post'),
                       url(r'^get_count$', views.get_count, name='get_count'),
                       )
