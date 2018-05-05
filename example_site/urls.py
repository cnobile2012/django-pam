# -*- coding: utf-8 -*-
#
# example_site/urls.py
#

"""
django_pam URL Configuration

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
__docformat__ = "restructuredtext en"

try:
    from django.urls import include, re_path
except:
    from django.conf.urls import include, url as re_path

from django.views.static import serve
from django.contrib import admin
from django.conf import settings

from example_site.home.views import home_page_view
from django_pam.accounts.views import LoginView, LogoutView

admin.autodiscover()


urlpatterns = [
    re_path(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^$', home_page_view, name='home-page'),
    re_path(r'^django-pam/', include('django_pam.urls')),
    re_path(r'^login/$', LoginView.as_view(template_name='home/login.html'),
        name='login'),
    re_path(r"^logout/(?P<next>[\w\-\:/]+)?$", LogoutView.as_view(
        template_name='home/logout.html'), name='logout')
    ]

if settings.DEBUG:
    # Static media files.
    import debug_toolbar

    urlpatterns += [
        re_path(r'^dev/(?P<path>.*)$', serve,
            {'document_root': settings.STATIC_URL, 'show_indexes': True}),
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
        ]
else:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve,
            {'document_root': settings.STATIC_URL, 'show_indexes': True}),
        ]
