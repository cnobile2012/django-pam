# -*- coding: utf-8 -*-
#
# django_pam/auth/tests/test_auth_backends.py
#

from ..backends import PAMBackend

from .base_test import BaseDjangoPAM


class TestPAMBackend(BaseDjangoPAM):

    def __init__(self, name):
        super(TestPAMBackend, self).__init__(name)

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
