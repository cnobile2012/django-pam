# -*- coding: utf-8 -*-
#
# django_pam/auth/backends.py
#

import types
import pam as pam_base

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _


class PAMBackend(object):
    _pam = pam_base.pam()

    def authenticate(self, username=None, password=None, email=None,
                     **extra_fields):
        PAMUser = get_user_model()
        user = None

        if self._pam.authenticate(username, password):
            try:
                user = PAMUser.objects.get(username=username)
            except PAMUser.DoesNotExist:
                user = PAMUser.objects.create_user(
                    username, email=None, **extra_fields)

        return user

    def get_user(self, user):
        PAMUser = get_user_model()
        obj = None

        if user.isdigit() and isinstance(int(user), (int, long)):
            query = models.Q(pk=user)
        elif isinstance(user, types.StringTypes):
            query = models.Q(username=user)
        else:
            raise TypeError(_("The user argument type should be either an "
                              "integer (pk) or a string (username), found "
                              "type {}.").format(type(user)))

        try:
            obj = PAMUser.objects.get(query)
        except PAMUser.DoesNotExist:
            pass

        return obj
