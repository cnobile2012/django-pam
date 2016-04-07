# -*- coding: utf-8 -*-
#
# fasbook/common/urls.py
#

from django.conf.urls import url
from django.views.generic import TemplateView

from .views import login_view, logout_view


urlpatterns = [
    url(r'^login/$', login_view, name='login'),
    #url(r'^logout/$', logout_view, name='logout'),
    ]
