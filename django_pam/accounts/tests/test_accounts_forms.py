# -*- coding: utf-8 -*-
#
# django_pam/auth/tests/test_auth_backends.py
#

import six

from django.test import RequestFactory
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

from ..forms import GeneralAuthenticationForm

from .base_test import BaseDjangoPAM


class TestGeneralAuthenticationForm(BaseDjangoPAM):

    def __init__(self, name):
        super(GeneralAuthenticationForm, self).__init__(name)
        self.factory = None

    def setUp(self):
        self.factory = RequestFactory()

    def test_user_created(self):
        """
        """
        #self.skipTest("Temporarily skipped")




