# -*- coding: utf-8 -*-
#
# django_pam/accounts/tests/test_accounts_forms.py
#

from django.utils import six
from django.test import RequestFactory
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AnonymousUser
from django.http import QueryDict

from django_pam.auth.tests.base_test import BaseDjangoPAM

from ..forms import AuthenticationForm


class TestAuthenticationForm(BaseDjangoPAM):

    def __init__(self, name):
        super(TestAuthenticationForm, self).__init__(name)
        self.factory = None

    def setUp(self):
        self.factory = RequestFactory()

    def test_user_created(self):
        """
        Test that the form created a user.

        Form constructor signature::

          __init__(self, request=None, *args, **kwargs)

        """
        #self.skipTest("Temporarily skipped")
        # Get user's credentials.
        username, password, email = self._prompt(need_email=True)
        # Setup request
        request = self.factory.get('django-pam:login')
        request.user = AnonymousUser()
        kwargs = {}
        data = kwargs.setdefault('data', QueryDict(mutable=True))
        data.appendlist('username', username)
        data.appendlist('password', password)
        data.appendlist('email', email)
        form = AuthenticationForm(**kwargs)
        msg = "kwargs: {}, errors: {}".format(kwargs, form.errors.as_data())
        self.assertTrue(form.is_valid(), msg)
        self.assertEqual(form.user_cache.username, username, msg)
        # Password should fail since it's never saved.
        self.assertFalse(form.user_cache.check_password(password), msg)
        self.assertEqual(form.user_cache.email, email, msg)

    def test_missing_credentials(self):
        """
        Test for missing credentials.
        """
        #self.skipTest("Temporarily skipped")
        # Get user's credentials.
        username, password, email = self._prompt(need_email=True)
        # Setup request
        request = self.factory.get('django-pam:login')
        request.user = AnonymousUser()
        kwargs = {}
        data = kwargs.setdefault('data', QueryDict(mutable=True))
        data.appendlist('username', username)
        data.appendlist('password', '')
        data.appendlist('email', email)
        form = AuthenticationForm(**kwargs)
        msg = "kwargs: {}, errors: {}".format(kwargs, form.errors.as_data())
        self.assertFalse(form.is_valid(), msg)
        # Check that we have a password and __all__ error messages.
        self.assertTrue('password' in form.errors.as_data(), msg)
        self.assertTrue('__all__' in form.errors.as_data(), msg)

    def test_invalid_credentials(self):
        """
        Test for invalid credentials.
        """
        #self.skipTest("Temporarily skipped")
        # Get user's credentials.
        username, password, email = "somebody", "password", "bad@email.net"
        request = self.factory.get('django-pam:login')
        request.user = AnonymousUser()
        kwargs = {}
        data = kwargs.setdefault('data', QueryDict(mutable=True))
        data.appendlist('username', username)
        data.appendlist('password', password)
        data.appendlist('email', email)
        form = AuthenticationForm(**kwargs)
        msg = "kwargs: {}, errors: {}".format(kwargs, form.errors.as_data())
        self.assertFalse(form.is_valid(), msg)
        self.assertTrue('__all__' in form.errors.as_data(), msg)
