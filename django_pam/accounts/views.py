#-*- coding: utf-8 -*-
#
# django_pam/accounts/views.py
#

import logging
import functools
import smtplib
import socket
import json

from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, login, logout, get_user_model)
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils.encoding import force_text
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import BaseListView
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import redirect, resolve_url
from django.conf import settings

from .forms import AuthenticationForm
from .view_mixins import JSONResponseMixin, AjaxableResponseMixin

log = logging.getLogger('django_pam.accounts.views')


#
# LoginView
#
class LoginView(AjaxableResponseMixin, FormView):
    """
    A class version of django.contrib.auth.views.login.

    Usage:
        url(r'^login/$', LoginView.as_view(
            form_class=MyAuthenticationForm,
            success_url='/my/success/url/),
            redirect_field_name='my-redirect-field-name'
            name='login'),
    """
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'django_pam/accounts/login.html'

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """
        Incoming AJAX data structure from an HTML <form> tag::

          [{'name': 'username', 'value': '<username>'},
           {'name': 'password', 'value': '<password>'},
           {'name': 'next', 'value': '<redirect URI>'}
          ]

        """
        if self.request.is_ajax():
            json_data = json.loads(self.request.body.decode('utf-8'))
            kwargs = {}
            data = {}

            for arg in json_data:
                name = arg.get('name')
                value = arg.get('value')

                if name == self.redirect_field_name:
                    self.success_url = reverse(value)
                else:
                    data[name] = value

            kwargs['data'] = data
        else:
            kwargs = super(LoginView, self).get_form_kwargs()

        return kwargs

    def form_valid(self, form):
        """
        The user has provided valid credentials (this was checked in the
        form's is_valid() method).
        """
        self.object = form.get_user()
        login(self.request, self.object)
        return super(LoginView, self).form_valid(form)

    def get_data(self, **context):
        # Called in form_valid in AjaxableResponseMixin.
        context.update({'username': self.object.get_username(),
                        'full_name': self.object.get_full_name(),
                        self.redirect_field_name: self.get_success_url()})
        return super(LoginView, self).get_data(**context)

    def get_success_url(self):
        if self.success_url:
            redirect_to = self.success_url
        else:
            redirect_to = self.request.GET.get(self.redirect_field_name, '')

        if not redirect_to:
            redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

        return redirect_to


#
# LogoutView
#
class LogoutView(JSONResponseMixin, TemplateView):
    template_name = "django_pam/accounts/logout.html"
    redirect_field_name = REDIRECT_FIELD_NAME
    success_url = settings.LOGIN_URL

    def get(self, request, *args, **kwargs):
        log.debug("request: %s, args: %s, kwargs: %s", request, args, kwargs)

        if not request.user.is_authenticated():
            response = redirect(self.get_success_url())
        else:
            next_page = request.GET.get(self.redirect_field_name, '')
            kwargs[self.redirect_field_name] = next_page
            context = self.get_context_data(**kwargs)
            response = self.render_to_response(context)

        return response

    def post(self, request, *args, **kwargs):
        """
        Incoming AJAX data structure from an HTML <form> tag:

        [{'name': 'next', 'value': '<redirect URI>'}]
        """
        log.debug("request: %s, args: %s, kwargs: %s", request, args, kwargs)
        next_page = request.POST.get(self.redirect_field_name, '')
        kwargs[self.redirect_field_name] = next_page
        self.success_url = next_page

        if request.user.is_authenticated():
            logout(request)

        if self.request.is_ajax():
            response = self.render_to_json_response({})
        else:
            response = redirect(self.get_success_url())

        return response

    def get_data(self, **context):
        # Called in JSONResponseMixin.
        context = super(LogoutView, self).get_data(**context)
        json_data = json.loads(self.request.body.decode('utf-8'))
        log.debug("json_data: %s", json_data)

        for arg in json_data:
            name = arg.get('name')
            value = arg.get('value')

            if name == self.redirect_field_name:
                context[name] = reverse(value)
            else:
                context[name] = value

        log.debug("context: %s, success_url: %s", context, self.success_url)
        return context

    def get_context_data(self, **kwargs):
        context = super(LogoutView, self).get_context_data(**kwargs)
        log.debug("kwargs: %s, context: %s", kwargs, context)
        context.update({
            self.redirect_field_name: kwargs.get(self.redirect_field_name),
            })
        return context

    def get_success_url(self):
        """
        Returns the supplied success URL.
        """
        if self.success_url:
            # Forcing possible reverse_lazy evaluation
            url = force_text(self.success_url)
        else:
            raise ImproperlyConfigured(
                _("No URL to redirect to. Provide a success_url."))

        return url
