from django.conf.urls import url
from . import views

#You can get more information about built-in authentication views at
#https://docs.djangoproject.com/en/1.8/topics/auth/default/#module-django.contrib.auth.views.

urlpatterns = [
               #previous login view
               #url(r'^login/$', views.user_login, name = 'login'),
               
               #blog posts views
               url(r'^index/$', views.post_list, name='post_list'),
               url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'\
                   r'(?P<post>[-\w]+)/$',
                   views.post_detail,
                   name='post_detail'),
               url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.post_list, name='post_list_by_tag'),
]


