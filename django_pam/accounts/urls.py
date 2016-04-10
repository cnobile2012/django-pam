# -*- coding: utf-8 -*-
#
# django_pam/accounts/urls.py
#

from django.conf.urls import url
from django.views.generic import TemplateView

from .views import LoginView, LogoutView


urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r"^logout/(?P<next>[\w\-\:/]+)?$", LogoutView.as_view(),
        name='logout'),
    ]
