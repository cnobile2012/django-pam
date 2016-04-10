#-*- coding: utf-8 -*-
#
# example_site/home/views.py
#

import logging

from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.urlresolvers import reverse

log = logging.getLogger('example.home.views')


#
# Home
#
class HomePageView(TemplateView):
    template_name = "home/home.html"
    redirect_field_name = REDIRECT_FIELD_NAME

    def dispatch(self, *args, **kwargs):
        # Either way works, with or with out the reverse function.
        #kwargs[self.redirect_field_name] = reverse('home-page')
        kwargs[self.redirect_field_name] = 'home-page'
        return super(HomePageView, self).dispatch(*args, **kwargs)

home_page_view = HomePageView.as_view()
