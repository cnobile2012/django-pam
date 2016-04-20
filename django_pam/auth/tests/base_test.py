# -*- coding: utf-8 -*-
#
# django_pam/auth/tests/base_test.py
#

import os
import sys
import six
from io import open
import getpass

from django.test import TestCase


class BaseDjangoPAM(TestCase):
    _CONFIG = '.django_pam'

    def __init__(self, name):
        super(BaseDjangoPAM, self).__init__(name)

    def _prompt(self, need_email=False):
        home = os.path.join(os.getenv('HOME'), self._CONFIG)
        fields = ('username', 'password', 'email',)
        lines = {}

        if os.path.exists(home):
            with open(home, 'rb') as file:
                for idx, line in enumerate(file):
                    lines[fields[idx]] = line.decode('utf-8').strip()

            username = lines.get('username')
            password = lines.get('password')
            email = lines.get('email')
        else:
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
