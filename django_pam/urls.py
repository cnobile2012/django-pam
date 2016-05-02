# -*- coding: utf-8 -*-
#
# django_pam/urls.py
#
"""
Django PAM urls.py
"""
__docformat__ = "restructuredtext en"


from django.conf.urls import include, url


urlpatterns = [
    url(r'^', include('django_pam.accounts.urls', namespace='django-pam')),
    ]
