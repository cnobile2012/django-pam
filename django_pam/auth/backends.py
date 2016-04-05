# -*- coding: utf-8 -*-
#
# django_pam/auth/backends.py
#

import types
import pam as pam_base

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.backends import ModelBackend


class PAMBackend(ModelBackend):
    _pam = pam_base.pam()

    def authenticate(self, username=None, password=None, email=None,
                     **extra_fields):
        """
        Authenticate using PAM then get the account if it exists else create
        a new account.

        :param username: The users username. This is a manditory field.
        :type username: str
        :param password: The users password. This is a manditory field.
        :type password: str
        :param email: The users email address.
        :type email: str
        :param extra_fields: Additonal keyword options of any editable field
                             in the user model.
        :rtype: The Django user object.
        """
        UserModel = get_user_model()
        user = None

        if self._pam.authenticate(username, password):
            try:
                user = UserModel._default_manager.get(username=username)
            except UserModel.DoesNotExist:
                user = UserModel.objects.create_user(
                    username, email=None, **extra_fields)

        return user

    def get_user(self, user):
        """
        Get the user by either the ``username`` or the ``pk``.

        :param user: The username or pk.
        :type user: str or int
        :rtype: The Django user object.
        """
        UserModel = get_user_model()
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
            obj = UserModel._default_manager.get(query)
        except UserModel.DoesNotExist:
            pass

        return obj
