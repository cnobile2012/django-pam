# -*- coding: utf-8 -*-
#
# django_pam/accounts/tests/test_accounts_forms.py
#

import json
import six

from django.test import Client

from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured

from django_pam.auth.tests.base_test import BaseDjangoPAM

from ..views import LoginView, LogoutView


class TestLoginView(BaseDjangoPAM):

    def __init__(self, name):
        super(TestLoginView, self).__init__(name)
        self.client = None

    def setUp(self):
        self.client = Client()

    def test_get_login_screen(self):
        """
        Test that the login screen returns properly.
        """
        #self.skipTest("Temporarily skipped")
        url = reverse('django-pam:login')
        response = self.client.get(url)
        msg = "response status: {}, should be 200".format(response.status_code)
        self.assertEqual(response.status_code, 200, msg)
        content = response.content.decode('utf-8')
        msg = "content: {}".format(content)
        self.assertTrue('csrfmiddlewaretoken' in content, msg)
        self.assertTrue('username' in content, msg)
        self.assertTrue('password' in content, msg)

    def test_post_login_form_valid(self):
        """
        Test that a valid form login returns a redirect properly.
        """
        #self.skipTest("Temporarily skipped")
        # Get user's credentials.
        username, password, email = self._prompt(need_email=True)
        # Setup request
        url = reverse('django-pam:login')
        data = {'username': username, 'password': password, 'email': email}
        response = self.client.post(url, data=data)
        msg = "response status: {}, should be 302".format(response.status_code)
        self.assertEqual(response.status_code, 302, msg)
        # Redirect
        response = self.client.get(response.url)
        msg = "response status: {}, should be 200".format(response.status_code)
        self.assertEqual(response.status_code, 200, msg)
        content = response.content.decode('utf-8')
        msg = "content: {}".format(content)
        self.assertTrue('you are Authenticated' in content, msg)
        self.assertEqual(content.count('?next=home-page'), 2, msg)

    def test_post_login_form_invalid_redirection(self):
        """
        Test that redirection will not take you off site.
        """
        #self.skipTest("Temporarily skipped")
        # Get user's credentials.
        username, password, email = self._prompt(need_email=True)
        # Setup request
        url = reverse('django-pam:login')
        data = {'username': username, 'password': password, 'email': email}
        response = self.client.post(url, data=data)
        msg = "response status: {}, should be 302".format(response.status_code)
        self.assertEqual(response.status_code, 302, msg)
        # Redirect to bad location
        off_site_url = "http://someplace.else.com/bad-page/"
        response = self.client.get(off_site_url)
        msg = "response status: {}, should be 404".format(response.status_code)
        self.assertEqual(response.status_code, 404, msg)
        content = response.content.decode('utf-8')
        msg = "content: {}".format(content)
        self.assertTrue('The requested URL /bad-page/' in content, msg)

    def test_post_login_form_invalid(self):
        """
        Test that an invalid form login returns a redirect properly.
        """
        #self.skipTest("Temporarily skipped")
        # Get user's credentials.
        username = password = email = ''
        # Setup request and test
        url = reverse('django-pam:login')
        data = {'username': username, 'password': password, 'email': email}
        response = self.client.post(url, data=data)
        msg = "response status: {}, should be 200".format(response.status_code)
        self.assertEqual(response.status_code, 200, msg)
        self.assertTrue(self._has_error(response))
        tests = {'__all__': "Please enter a correct",
                 'username': 'This field is required.',
                 'password': 'This field is required.'}
        self._test_errors(response, tests=tests)
        # Check with invalid username and password.
        username = 'InvalidUsername'
        password = 'InvalidPassword'
        email = 'junk'
        data = {'username': username, 'password': password, 'email': email}
        response = self.client.post(url, data=data)
        msg = "response status: {}, should be 200".format(response.status_code)
        self.assertEqual(response.status_code, 200, msg)
        self.assertTrue(self._has_error(response))
        tests = {'__all__': "Please enter a correct",
                 'email': "Enter a valid email address."}
        self._test_errors(response, tests=tests)

    def test_post_login_ajax_valid(self):
        """
        Test that a valid AJAX login returns a redirect properly.
        """
        #self.skipTest("Temporarily skipped")
        # Get user's credentials.
        username, password, email = self._prompt(need_email=True)
        # Setup request
        url = reverse('django-pam:login')
        data = json.dumps([
            {'name': 'username', 'value': username},
            {'name': 'password', 'value': password},
            {'name': 'email', 'value': email},
            ])
        response = self.client.post(url, content_type='application/json',
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                                    data=data)
        self.assertFalse(self._has_error(response))
        # JavaScript does the redirect, so a 200 OK is valid here.
        msg = "response status: {}, should be 200".format(response.status_code)
        self.assertEqual(response.status_code, 200, msg)
        content = json.loads(response.content.decode('utf-8'))
        msg = "content: {}".format(content)
        self.assertTrue(content.get('full_name', '') == '', msg)
        self.assertTrue(content.get('username', '') == username, msg)
        self.assertTrue(content.get('next', '') == '/', msg)

    def test_post_login_ajax_invalid(self):
        """
        Test that an invalid AJAX login returns a redirect properly.
        """
        #self.skipTest("Temporarily skipped")
        # Get user's credentials.
        username = password = email = ''
        # Setup request
        url = reverse('django-pam:login')
        data = json.dumps([
            {'name': 'username', 'value': username},
            {'name': 'password', 'value': password},
            {'name': 'email', 'value': email},
            ])
        response = self.client.post(url, content_type='application/json',
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                                    data=data)
        self.assertFalse(self._has_error(response))
        tests = {'__all__': "Please enter a correct",
                 'username': 'This field is required.',
                 'password': 'This field is required.'}
        self._test_errors(response, tests=tests)
        # Check with invalid username and password.
        username = 'InvalidUsername'
        password = 'InvalidPassword'
        email = 'junk'
        data = json.dumps([
            {'name': 'username', 'value': username},
            {'name': 'password', 'value': password},
            {'name': 'email', 'value': email}
            ])
        response = self.client.post(url, content_type='application/json',
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                                    data=data)
        msg = "response status: {}, should be 400".format(response.status_code)
        self.assertEqual(response.status_code, 400, msg)
        tests = {'__all__': "Please enter a correct",
                 'email': "Enter a valid email address."}
        self._test_errors(response, tests=tests)


class TestLogoutView(BaseDjangoPAM):

    def __init__(self, name):
        super(TestLogoutView, self).__init__(name)
        self.client = None

    def setUp(self):
        self.client = Client()

    def _login_form(self):
        # Get user's credentials.
        username, password, email = self._prompt(need_email=True)
        # Setup request
        url = reverse('django-pam:login')
        data = {'username': username, 'password': password, 'email': email}
        response = self.client.post(url, data=data)
        msg = "response status: {}, should be 302".format(response.status_code)
        self.assertEqual(response.status_code, 302, msg)

    def _login_ajax(self):
        username, password, email = self._prompt(need_email=True)
        # Setup request
        url = reverse('django-pam:login')
        data = json.dumps([
            {'name': 'username', 'value': username},
            {'name': 'password', 'value': password},
            {'name': 'email', 'value': email},
            {'name': 'next', 'value': 'home-page'},
            ])
        response = self.client.post(url, content_type='application/json',
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                                    data=data)
        self.assertFalse(self._has_error(response))
        # JavaScript does the redirect, so a 200 OK is valid here.
        msg = "response status: {}, should be 200".format(response.status_code)
        self.assertEqual(response.status_code, 200, msg)

    def test_get_logout_screen(self):
        """
        Test that the logout screen returns properly.
        """
        #self.skipTest("Temporarily skipped")
        # Test that user is not logged in.
        url = reverse('django-pam:logout') + '?next=home-page'
        response = self.client.get(url)
        msg = "response status: {}, should be 302".format(response.status_code)
        self.assertEqual(response.status_code, 302, msg)
        # Create user
        self._login_form()
        url = reverse('django-pam:logout') + '?next=home-page'
        response = self.client.get(url)
        msg = "response status: {}, should be 200".format(response.status_code)
        self.assertEqual(response.status_code, 200, msg)
        content = response.content.decode('utf-8')
        msg = "content: {}".format(content)
        self.assertTrue('csrfmiddlewaretoken' in content, msg)
        self.assertTrue('next' in content, msg)

    def test_post_logout_form(self):
        """
        Test that a valid form logout returns a redirect properly.
        """
        #self.skipTest("Temporarily skipped")
        # Create user
        self._login_form()
        # Setup request
        url = reverse('django-pam:logout')
        data = {'next': 'home-page'}
        response = self.client.post(url, data=data)
        msg = "response status: {}, should be 302".format(response.status_code)
        self.assertEqual(response.status_code, 302, msg)
        # Redirect
        response = self.client.get(response.url)
        msg = "response status: {}, should be 200".format(response.status_code)
        self.assertEqual(response.status_code, 200, msg)
        content = response.content.decode('utf-8')
        msg = "content: {}".format(content)
        self.assertTrue('Welcome, Please Login' in content, msg)

    def test_post_logout_form_invalid(self):
        """
        Test that if the success_url is not set an exception is raised.
        """
        #self.skipTest("Temporarily skipped")
        # Create user
        self._login_form()
        # Setup request
        url = reverse('django-pam:logout')
        data = {'next': ''}
        with self.assertRaises(ImproperlyConfigured) as cm:
            response = self.client.post(url, data=data)

    def test_post_logout_ajax(self):
        """
        Test that a valid ajax logout returns properly.
        """
        #self.skipTest("Temporarily skipped")
        # Create user
        self._login_ajax()
        # Setup request
        url = reverse('django-pam:logout')
        value0 = {'name': 'next', 'value': 'home-page'}
        value1 = {'name': 'user', 'value': 'realuser'}
        data = json.dumps([value0, value1])
        response = self.client.post(url, content_type='application/json',
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                                    data=data)
        self.assertFalse(self._has_error(response))
        # JavaScript does the redirect, so a 200 OK is valid here.
        msg = "response status: {}, should be 200".format(response.status_code)
        self.assertEqual(response.status_code, 200, msg)
        content = json.loads(response.content.decode('utf-8'))
        redirect_uri = reverse(value0.get('value'))
        user = value1.get('value')
        msg = "content: {}, redirect_uri: {}, user: {}".format(
            content, redirect_uri, user)
        self.assertEqual(redirect_uri, content.get('next'), msg)
        self.assertEqual(user, content.get('user'), msg)
