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

from django.conf.urls import include, url
from django.views.static import serve
from django.contrib import admin
from django.conf import settings

from example_site.home.views import home_page_view
from django_pam.accounts.views import LoginView, LogoutView

admin.autodiscover()


urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', home_page_view, name='home-page'),
    url(r'^django-pam/', include('django_pam.urls')),
    url(r'^login/$', LoginView.as_view(template_name='home/login.html'),
        name='login'),
    url(r"^logout/(?P<next>[\w\-\:/]+)?$", LogoutView.as_view(
        template_name='home/logout.html'), name='logout')
    ]

if settings.DEBUG:
    urlpatterns += [
    url(r'^dev/(?P<path>.*)$', serve,
        {'document_root': settings.STATIC_URL, 'show_indexes': True}),
    ]
else:
    urlpatterns += [
    url(r'^static/(?P<path>.*)$', serve,
        {'document_root': settings.STATIC_URL, 'show_indexes': True}),
    ]
