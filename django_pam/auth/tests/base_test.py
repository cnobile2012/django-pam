# -*- coding: utf-8 -*-
#
# django_pam/auth/tests/base_test.py
#

import os
import sys
import six
import types
import getpass

from io import open
from collections import OrderedDict

from django.test import TestCase
from django.utils.translation import ugettext


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

    def _clean_data(self, data):
        if data is not None:
            if isinstance(data, (list, tuple,)):
                data = self.__clean_value(data)
            else:
                for key in data:
                    data[key] = self.__clean_value(data.get(key))

        return data

    def __clean_value(self, value):
        if isinstance(value, (list, tuple,)):
            value = [self.__clean_value(item) for item in value]
        elif isinstance(value, (dict, OrderedDict,)):
            for key in value:
                value[key] = self.__clean_value(value.get(key))
        elif (isinstance(value, (int, long, bool, types.TypeType,)) or
              value is None):
            pass
        else:
            value = ugettext(value)

        return value
