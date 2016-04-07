#-*- coding: utf-8 -*-
#
# django_pam/accounts/views.py
#
# I give credit to stefanfoulis at:
#  https://github.com/stefanfoulis/django-class-based-auth-views/
#

import logging
import functools
import smtplib
import socket
import json

try:
    import urlparse
except ImportError:
    from urllib import parse as urlparse # python3 support

from django.core.mail import send_mail
from django.core.exceptions import SuspiciousOperation
from django.contrib.auth import REDIRECT_FIELD_NAME, login, get_user_model
from django.contrib.auth.models import Group
from django.contrib import auth
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.views.generic.base import TemplateResponseMixin
from django.views.generic import View, TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import BaseListView
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import redirect, resolve_url
from django.conf import settings

from .forms import GeneralAuthenticationForm

log = logging.getLogger('django_pam.accounts.views')


#
# LoginView
#
class LoginView(FormView):
    """
    This is a class based version of django.contrib.auth.views.login.

    Usage:
      in urls.py:
        url(r'^login/$', LoginView.as_view(
            form_class=MyCustomAuthFormClass,
            success_url='/my/custom/success/url/),
            name='login'),
    """
    form_class = GeneralAuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'django_pam/accounts/login.html'

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        """
        The user has provided valid credentials (this was checked in
        AuthenticationForm.is_valid()). So now we can check the test cookie
        stuff and log him in.
        """
        self.check_and_delete_test_cookie()
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def form_invalid(self, form):
        """
        The user has provided invalid credentials (this was checked in
        AuthenticationForm.is_valid()). So now we set the test cookie again
        and re-render the form with errors.
        """
        self.set_test_cookie()
        return super(LoginView, self).form_invalid(form)

    def get_success_url(self):
        if self.success_url:
            redirect_to = self.success_url
        else:
            redirect_to = self.request.GET.get(self.redirect_field_name, '')

        netloc = urlparse.urlparse(redirect_to)[1]

        if not redirect_to:
            redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
        # Security check -- don't allow redirection to a different host.
        elif netloc and netloc != self.request.get_host():
            redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

        return redirect_to

    def set_test_cookie(self):
        self.request.session.set_test_cookie()

    def check_and_delete_test_cookie(self):
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
            return True

        return False

    def get(self, request, *args, **kwargs):
        """
        Same as django.views.generic.edit.ProcessFormView.get(), but adds test
        cookie stuff
        """
        self.set_test_cookie()
        return super(LoginView, self).get(request, *args, **kwargs)


#
# LogoutView
#
class LogoutView(TemplateResponseMixin, View):
    template_name = "django_pam/accounts/logout.html"
    http_method_names = ('post',)

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            auth.logout(self.request)

        return self.render_to_response({})


## class LogoutView(TemplateResponseMixin, View):
##     template_name = "registration/logout.html"
##     redirect_field_name = "next"

##     def get(self, *args, **kwargs):
##         if not self.request.user.is_authenticated():
##             return redirect(self.get_redirect_url())
##         context = self.get_context_data()
##         return self.render_to_response(context)

##     def post(self, *args, **kwargs):
##         if self.request.user.is_authenticated():
##             auth.logout(self.request)
##         return redirect(self.get_redirect_url())

##     def get_context_data(self, **kwargs):
##         context = kwargs
##         redirect_field_name = self.get_redirect_field_name()
##         context.update({
##             "redirect_field_name": redirect_field_name,
##             "redirect_field_value": self.request.REQUEST.get(redirect_field_name),
##             })
##         return context

##     def get_redirect_field_name(self):
##         return self.redirect_field_name

##     def get_redirect_url(self, fallback_url=None, **kwargs):
##         if fallback_url is None:
##             fallback_url = settings.LOGIN_URL
##         kwargs.setdefault("redirect_field_name", self.get_redirect_field_name())
##         return default_redirect(self.request, fallback_url, **kwargs)
