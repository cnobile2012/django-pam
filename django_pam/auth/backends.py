# -*- coding: utf-8 -*-
#
# django_pam/auth/backends.py
#

import logging
import types
import six
import pam as pam_base

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.backends import ModelBackend

log = logging.getLogger('django_pam.auth.backends')


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
        log.debug("username: %s, email: %s, extra_fields: %s",
                  username, email, extra_fields)
        UserModel = get_user_model()
        user = None

        if self._pam.authenticate(username, password):
            try:
                user = UserModel._default_manager.get_by_natural_key(
                    username=username)
            except UserModel.DoesNotExist:
                user = UserModel.objects.create_user(
                    username, email=email, **extra_fields)

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

        if user is not None and (isinstance(user, (int, long)) or
                                 user.isdigit()):
            query = models.Q(pk=user)
        elif isinstance(user, six.string_types):
            query = models.Q(username=user) | models.Q(email=user)
        else:
            raise TypeError(_("The user argument type should be either an "
                              "integer (valid pk) or a string (username or "
                              "email), found type {}.").format(type(user)))

        try:
            obj = UserModel._default_manager.get(query)
        except UserModel.DoesNotExist:
            pass

        log.debug("user: %s, obj: %s", user, obj)
        return obj
