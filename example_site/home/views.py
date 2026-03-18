# -*- coding: utf-8 -*-
#
# example_site/home/views.py
#

import logging

from django.views.generic import TemplateView
from django.contrib.auth import REDIRECT_FIELD_NAME

log = logging.getLogger('example.home.views')


class HomePageView(TemplateView):
    """
    Home
    """
    template_name = "home/home.html"
    redirect_field_name = REDIRECT_FIELD_NAME

    def dispatch(self, *args, **kwargs):
        # Either way works, with or with out the reverse function.
        kwargs[self.redirect_field_name] = 'home-page'
        return super().dispatch(*args, **kwargs)


home_page_view = HomePageView.as_view()
