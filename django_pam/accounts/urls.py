# -*- coding: utf-8 -*-
#
# django_pam/accounts/urls.py
#

"""
Django PAM accounta/urls.py
"""
__docformat__ = "restructuredtext en"

try:
    from django.urls import re_path
except Exception:
    from django.conf.urls import url as re_path

from .views import LoginView, LogoutView


urlpatterns = [
    re_path(r'^login/$', LoginView.as_view(), name='login'),
    re_path(r'^logout/$', LogoutView.as_view(), name='logout'),
    ]
