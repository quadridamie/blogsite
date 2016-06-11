"""bookmarks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from account import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^account/', include('account.urls', namespace='account', app_name='account')),
   
   #login/logout views
    url(r'^account/login/$', 'django.contrib.auth.views.login', name="login"),
    url(r'^account/logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^account/logout-then-login/$', 'django.contrib.auth.views.logout_then_login', name='logout_then_login'),
    url(r'^account/dashboard', views.dashboard, name='dashboard'),
               
    #change password urls
    url(r'^account/password-change/$','django.contrib.auth.views.password_change', name='password_change'),
    url(r'^account/password-change/done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
               
    #restore password urls
    url(r'^account/password-reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    url(r'^account/password-reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^account/password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
                   'django.contrib.auth.views.password_reset_confirm',
                   name='password_reset_confirm'),
    url(r'^account/password-reset/complete/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),
               
    #user registration
    url(r'^account/register/$', views.register, name='register'),
              
    #user profile edit
    url(r'^account/edit/$', views.edit, name='edit'),
    
    #Social auth url
    url('social-auth/', include('social.apps.django_app.urls', namespace='social')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)