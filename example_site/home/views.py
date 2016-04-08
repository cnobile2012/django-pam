#-*- coding: utf-8 -*-
#
# example_site/home/views.py
#

import logging

from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

log = logging.getLogger('example.home.views')


#
# Home
#
class HomePageView(TemplateView):
    template_name = "home/home.html"

    def dispatch(self, *args, **kwargs):
        return super(HomePageView, self).dispatch(*args, **kwargs)

home_page_view = HomePageView.as_view()