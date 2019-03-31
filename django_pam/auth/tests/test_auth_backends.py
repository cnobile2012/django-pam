# -*- coding: utf-8 -*-
#
# django_pam/auth/tests/test_auth_backends.py
#

from django.contrib.auth import get_user_model

from ..backends import PAMBackend

from .base_test import BaseDjangoPAM


class TestPAMBackend(BaseDjangoPAM):

    def __init__(self, name):
        super(TestPAMBackend, self).__init__(name)

    def setUp(self):
        self.pam = PAMBackend()

    def test_authenticate_pass(self):
        """
        Test that authenticate method works properly.
        """
        #self.skipTest("Temporarily skipped")
        # Get user's credentials.
        username, password, email = self._prompt()
        # Test auth
        user = self.pam.authenticate(
            None, username=username, password=password)
        msg = "username: {}, user object: {}".format(username, user)
        self.assertEqual(user.username, username, msg)

    def test_authenticate_pass_service(self):
        """
        Test that authenticate method works properly with 'service'
        passed in.
        """
        #self.skipTest("Temporarily skipped")
        # Get user's credentials.
        username, password, email = self._prompt()
        # Test auth
        user = self.pam.authenticate(
            None, username=username, password=password, service='passwd')
        msg = "username: {}, user object: {}".format(username, user)
        self.assertEqual(user.username, username, msg)

    def test_authenticate_pass_encoding(self):
        """
        Test that authenticate method works properly with 'encoding'
        passed in.
        """
        #self.skipTest("Temporarily skipped")
        # Get user's credentials.
        username, password, email = self._prompt()
        # Test auth
        user = self.pam.authenticate(
            None, username=username, password=password, encoding='ascii')
        msg = "username: {}, user object: {}".format(username, user)
        self.assertEqual(user.username, username, msg)

    def test_authenticate_pass_resetcreds(self):
        """
        Test that authenticate method works properly with 'resetcreds'
        passed in.
        """
        #self.skipTest("Temporarily skipped")
        # Get user's credentials.
        username, password, email = self._prompt()
        # Test auth
        user = self.pam.authenticate(
            None, username=username, password=password, resetcreds=False)
        msg = "username: {}, user object: {}".format(username, user)
        self.assertEqual(user.username, username, msg)

    def test_authenticate_fail_invalid(self):
        """
        Test that authenticate fails with invalid credentials.
        """
        #self.skipTest("Temporarily skipped")
        # Get user's credentials.
        username, password, email = "username", "password", "email"
        # Test auth
        user = self.pam.authenticate(
            None, username=username, password=password)
        msg = "username: {}, user object: {}".format(username, user)
        self.assertIsNone(user, msg)

    def test_get_user_valid(self):
        """
        Test that the ``PAMBackend.authenticate()`` method works properly.
        """
        #self.skipTest("Temporarily skipped")
        # Get user's credentials.
        username, password, email = self._prompt(need_email=True)
        # Create user
        user = self.pam.authenticate(
            None, username=username, password=password, email=email)
        msg = "username: {}, user object: {}".format(username, user)
        self.assertEqual(user.username, username, msg)
        # Test get_user with username
        user = self.pam.get_user(username)
        pk = user.pk
        msg = "username: {}, user: {}, email: {}".format(username, user, email)
        self.assertEqual(user.username, username, msg)
        # Test get_user with email
        user = self.pam.get_user(email)
        self.assertEqual(user.email, email, msg)
        # Test user with PK
        user = self.pam.get_user(pk)
        msg = "User PK: {}, obj PK: {}, email: {}".format(pk, user.pk, email)
        self.assertEqual(user.pk, pk, msg)
        # Test with a string representing an integer.
        user = self.pam.get_user(str(pk))
        self.assertEqual(user.pk, pk, msg)
        # Test that the exception gets raised
        with self.assertRaises(TypeError) as cm:
            self.pam.get_user(None)

    def test_get_user_invalid(self):
        """
        Test that an invalid user returns a ``None`` object.
        """
        #self.skipTest("Temporarily skipped")
        UserModel = get_user_model()
        # Test that the exception gets raised
        pk = 99999
        user = self.pam.get_user(pk)
        msg = "pk: {}, user: {}".format(pk, user)
        self.assertIsNone(user, msg)
