# -*- coding: utf-8 -*-
#
# fasbook/common/urls.py
#

from django.conf.urls import url
from django.views.generic import TemplateView

from .views import (
    home_page_view, login_view, logout_view, request_membership_update_view,
    site_admin_view)


urlpatterns = [
    url(r'^$', home_page_view, name='home'),
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^request-membership/(?P<username>.+)/$',
        request_membership_update_view, name='request-membership'),
    url(r'^site-admin/$', site_admin_view, name="site-admin"),
    ]
