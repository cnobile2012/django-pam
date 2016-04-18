# -*- coding: utf-8 -*-
#
# django_pam/auth/tests/test_auth_backends.py
#

import six
import sys
import getpass
import readline

from django.contrib.auth import get_user_model
from django.test import TestCase

from django_pam.auth.backends import PAMBackend


class TestPAMBackend(TestCase):

    def __init__(self, name):
        super(TestPAMBackend, self).__init__(name)

    def _prompt(self, need_email=False):
        temp_username = getpass.getuser()
        sys.stderr.write("Username ({}): ".format(temp_username))
        username = six.moves.input() # Prompt goes to stdout which is off.

        if not username:
            username = temp_username

        password = getpass.getpass()

        if need_email:
            sys.stderr.write("Email: ")
            email = six.moves.input() # Prompt goes to stdout which is off.
        else:
            email = None

        return username, password, email

    def setUp(self):
        self.pam = PAMBackend()

    def test_authenticate(self):
        """
        Test that the ``PAMBackend.authenticate()`` method works properly.
        """
        #self.skipTest("Temporarily skipped")
        # Get user's credentials.
        username, password, email = self._prompt()
        # Test auth
        user = self.pam.authenticate(username=username, password=password)
        msg = "username: {}, user object: {}".format(username, user)
        self.assertTrue(user, msg)

    def test_get_user(self):
        """
        Test that the ``PAMBackend.authenticate()`` method works properly.
        """
        #self.skipTest("Temporarily skipped")
        # Get user's credentials.
        username, password, email = self._prompt(need_email=True)
        # Create user
        user = self.pam.authenticate(username=username, password=password,
                                     email=email)
        msg = "username: {}, user object: {}".format(username, user)
        self.assertTrue(user, msg)
        # Test get_user with username
        user = self.pam.get_user(username)
        pk = user.pk
        msg = "username: {}, user: {}, email: {}".format(username, user, email)
        self.assertEqual(username, user.username, msg)
        # Test get_user with email
        user = self.pam.get_user(email)
        self.assertEqual(email, user.email, msg)
        # Test user with PK
        user = self.pam.get_user(pk)
        msg = "User PK: {}, obj PK: {}, email: {}".format(pk, user.pk, email)
        self.assertEqual(pk, user.pk, msg)
        # Test with a string representing an integer.
        user = self.pam.get_user(str(pk))
        self.assertEqual(pk, user.pk, msg)
        # Tes that the exception gets raised
        with self.assertRaises(TypeError) as cm:
            self.pam.get_user(None)
