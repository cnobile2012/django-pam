# -*- coding: utf-8 -*-
#
# django_pam/accounts/tests/test_accounts_forms.py
#

import six

from django.test import Client

from django.core.urlresolvers import reverse

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
        self.assertEquals(response.status_code, 200, msg)
        content = response.content.decode('utf-8')
        self.assertTrue('csrfmiddlewaretoken' in content, msg)
        self.assertTrue('username' in content, msg)
        self.assertTrue('password' in content, msg)





