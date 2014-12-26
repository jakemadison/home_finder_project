from django.conf.urls import patterns, url
from datagetter import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^mobile$', views.mobile_index, name='mobile'),
                       url(r'^new$', views.new_index, name='new'),
                       url(r'^saved_posts$', views.saved_posts, name='saved_posts'),
                       url(r'^all_posts$', views.all_posts, name='all_posts'),
                       url(r'^rate_post$', views.rate_post, name='rate_post'),
                       url(r'^get_count$', views.get_count, name='get_count'),
                       url(r'^delete_post$', views.delete_post, name='delete_post'),

                       )
