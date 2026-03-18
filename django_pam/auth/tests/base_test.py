# -*- coding: utf-8 -*-
#
# django_pam/auth/tests/base_test.py
#

import os
import sys
import json
import types
import getpass

from io import open
from collections import OrderedDict

from django.conf import settings
from django.test import TestCase
from django.utils.translation import gettext
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseDjangoPAM(TestCase):
    _CONFIG = '.django_pam'

    def __init__(self, name):
        super().__init__(name)

    def _prompt(self, need_email=False):
        home = os.path.join(settings.BASE_DIR, '..', self._CONFIG)
        fields = ('username', 'password', 'email',)
        lines = {}

        if os.path.exists(home):
            with open(home, 'rb') as file:
                for idx, line in enumerate(file):
                    lines[fields[idx]] = line.decode('utf-8').strip()

            username = lines.get('username')
            password = lines.get('password')
            email = lines.get('email')
        else:  # pragma: no cover
            temp_username = getpass.getuser()
            sys.stderr.write("Username ({}): ".format(temp_username))
            username = input()  # Prompt goes to stdout which is off.

            if not username:
                username = temp_username

            password = getpass.getpass()

            if need_email:
                sys.stderr.write("Email: ")
                email = input()  # Prompt goes to stdout which is off.
            else:
                email = None

        return username, password, email

    def _create_user(self, username='', password='', email=''):
        # Get user's credentials.
        if username == '':
            username, password, email = self._prompt(need_email=True)

        User.objects.create_user(username=username, password=password)
        return username, password, email

    def _has_error(self, response):
        result = False

        if hasattr(response, 'context_data'):
            if response.context_data.get('form').errors:
                result = True

        return result

    def _test_errors(self, response, tests={}):
        if hasattr(response, 'context_data'):
            errors = dict(response.context_data.get('form').errors)

            for key, value in tests.items():
                err_msg = errors.pop(key, None)
                self.assertTrue(err_msg, "Could not find key: {}".format(key))
                err_msg = err_msg.as_text()
                msg = "For key '{}' value '{}' not found in '{}'".format(
                    key, value, err_msg)
                self.assertTrue(value in err_msg, msg)
        elif hasattr(response, 'content'):
            errors = json.loads(response.content.decode('utf-8'))

            for key, value in tests.items():
                err_msg = errors.pop(key, None)
                self.assertTrue(err_msg, "Could not find key: {}".format(key))
                msg = "For key '{}' value '{}' not found in '{}'".format(
                    key, value, err_msg)

                if isinstance(err_msg, (list, tuple)):
                    err_msg = err_msg[0]

                self.assertTrue(value in err_msg, msg)
        else:  # pragma: no cover
            msg = "No context_data"
            self.assertTrue(False, msg)

        msg = "Unaccounted for errors: {}".format(errors)
        self.assertFalse(len(errors) != 0 and True or False, msg)
