# -*- coding: utf-8 -*-
#
# django_pam/accounts/urls.py
#
"""
Django PAM accounta/urls.py


"""
__docformat__ = "restructuredtext en"


from django.conf.urls import url
from django.views.generic import TemplateView

from .views import LoginView, LogoutView


urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    ]
