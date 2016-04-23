#-*- coding: utf-8 -*-
#
# django_pam/accounts/forms.py
#

import logging
import inspect

from django import forms
from django.contrib.auth import get_user_model, get_backends
from django.contrib.auth.forms import AuthenticationForm as _AuthenticationForm

log = logging.getLogger('django_pam.accounts.forms')


class AuthenticationForm(_AuthenticationForm):
    """
    Authentication form
    """
    email = forms.EmailField(required=False, label_suffix='')

    def __init__(self, request=None, *args, **kwargs):
        log.debug("request: %s, args: %s, kwargs: %s, dir(self): %s",
                  request, args, kwargs, dir(self))
        self.base_fields['username'].label_suffix = ''
        self.base_fields['password'].label_suffix = ''
        super(AuthenticationForm, self).__init__(
            request=request, *args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        email = self.cleaned_data.get('email')

        if username and password:
            self.user_cache = self.authenticate(username=username,
                                                password=password)

            if self.user_cache:
                if email:
                    self.user_cache.email = email
                    self.user_cache.save()

                self.confirm_login_allowed(self.user_cache)

        if not (username and password and self.user_cache):
            raise forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={'username': self.username_field.verbose_name},
                )

        return self.cleaned_data

    def authenticate(self, **credentials):
        """
        If the given credentials are valid, return a User object.
        """
        user = None

        for backend in get_backends():
            try:
                inspect.getcallargs(backend.authenticate, **credentials)
            except TypeError:
                # This backend doesn't accept these credentials as arguments.
                # Try the next one.
                continue

            try:
                user = backend.authenticate(**credentials)
            except PermissionDenied:
                # This backend says to stop in our tracks - this user should
                # not be allowed in at all. (user is None)
                break
            else:
                if user:
                    # Annotate the user object with the path of the backend.
                    # (user is a valid object)
                    user.backend = "{}.{}".format(backend.__module__,
                                                  backend.__class__.__name__)
                    break

        return user

    class Media:
        css = {
            'all': ('django_pam/css/auth.css',)
            }
        js = ('django_pam/js/auth.js',)
