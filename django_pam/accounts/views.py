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
from django.core.urlresolvers import reverse
from django.core.exceptions import SuspiciousOperation
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, login, logout, get_user_model)
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
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
# RedirectMixin
#
class RedirectMixin(object):

    def default_redirect(self, fallback_url, **kwargs):
        """
        Evaluates a redirect url by consulting GET, POST and the session.
        """
        log.debug("fallback_url: %s, kwargs: %s", fallback_url, kwargs)
        redirect_field_name = kwargs.get("redirect_field_name", "next")

        if self.request.method.upper() == 'POST':
            next = self.request.POST.get(redirect_field_name)
        else:
            next = self.request.GET.get(redirect_field_name)

        if not next:
            # try the session if available
            if hasattr(self.request, "session"):
                session_key_value = kwargs.get("session_key_value",
                                               "redirect_to")
                next = self.request.session.get(session_key_value)

        is_safe = functools.partial(
            self.ensure_safe_url,
            allowed_schemas=kwargs.get("allowed_schemas"),
            allowed_host=self.request.get_host()
            )

        redirect_to = reverse(next if next and is_safe(next) else fallback_url)
        # perform one last check to ensure the URL is safe to redirect to. if it
        # is not then we should bail here as it is likely developer error and
        # they should be notified
        is_safe(redirect_to, raise_on_fail=True)
        return redirect_to

    def ensure_safe_url(self, url, allowed_schemas=None, allowed_host=None,
                        raise_on_fail=False):
        log.debug("url: %s", url)

        if allowed_schemas is None:
            allowed_schemas = ["http", "https"]

        parsed = urlparse.urlparse(url)
        # perform security checks to ensure no malicious intent
        # (i.e., an XSS attack with a data URL)
        safe = True

        if parsed.scheme and parsed.scheme not in allowed_schemas:
            if raise_on_fail:
                msg = _("Unsafe redirect to URL with protocol '{}'").format(
                    parsed.scheme)
                raise SuspiciousOperation(msg)

            safe = False

        if allowed_host and parsed.netloc and parsed.netloc != allowed_host:
            if raise_on_fail:
                msg = _("Unsafe redirect to URL not matching host '{}'").format(
                    allowed_host)
                raise SuspiciousOperation(msg)

            safe = False

        return safe


#
# LogoutView
#
class LogoutView(RedirectMixin, TemplateView):
    template_name = "django_pam/accounts/logout.html"
    redirect_field_name = REDIRECT_FIELD_NAME
    pattern_name = None

    def get(self, request, *args, **kwargs):
        log.debug("request: %s, args: %s, kwargs: %s", request, args, kwargs)

        if not request.user.is_authenticated():
            result = redirect(self.get_redirect_url(*args, **kwargs))
        else:
            kwargs[self.redirect_field_name] = kwargs.get(
                self.redirect_field_name, '')
            context = self.get_context_data(**kwargs)
            result = self.render_to_response(context)

        return result

    def post(self, request, *args, **kwargs):
        log.debug("request: %s, args: %s, kwargs: %s", request, args, kwargs)

        if request.user.is_authenticated():
            logout(request)

        return redirect(self.get_redirect_url(*args, **kwargs))

    def get_context_data(self, **kwargs):
        log.debug("kwargs: %s", kwargs)
        context = super(LogoutView, self).get_context_data(**kwargs)
        context.update({
            self.redirect_field_name: kwargs.get(self.redirect_field_name),
            })
        return context

    def get_redirect_url(self, fallback_url=None, *args, **kwargs):
        if fallback_url is None:
            fallback_url = settings.LOGIN_URL

        kwargs['redirect_field_name'] = reverse(self.pattern_name, args=args,
                                                kwargs=kwargs)
        return self.default_redirect(fallback_url, **kwargs)
