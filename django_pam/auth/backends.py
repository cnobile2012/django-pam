# -*- coding: utf-8 -*-
#
# django_pam/auth/backends.py
#
"""
Django PAM views.
"""
__docformat__ = "restructuredtext en"

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
    """
    An implementation of a PAM backend authentication module.
    """
    _pam = pam_base.pam()

    def authenticate(self, username=None, password=None, **extra_fields):
        """
        Authenticate using PAM then get the account if it exists else create
        a new account.

        :param username: The users username. This is a manditory field.
        :type username: str
        :param password: The users password. This is a manditory field.
        :type password: str
        :param extra_fields: Additonal keyword options of any editable field
                             in the user model.
        :rtype: The Django user object.
        """
        log.debug("username: %s, extra_fields: %s", username, extra_fields)
        UserModel = get_user_model()
        user = None

        if self._pam.authenticate(username, password):
            try:
                user = UserModel._default_manager.get_by_natural_key(
                    username=username)
            except UserModel.DoesNotExist:
                user = UserModel._default_manager.create_user(
                    username, **extra_fields)

        return user

    def get_user(self, user_data):
        """
        Get the user by either the ``username``, ``email``, or the ``pk``.

        :param user_data: The username, email or pk.
        :type user: str or int
        :rtype: A Django user object.
        """
        UserModel = get_user_model()
        obj = None

        if user_data is not None and (
            isinstance(user_data, six.integer_types) or
            user_data.isdigit()):
            query = models.Q(pk=user_data)
        elif isinstance(user_data, six.string_types):
            query = models.Q(username=user_data) | models.Q(email=user_data)
        else:
            msg = _("The user argument type should be either an integer "
                    "(valid pk) or a string (username or email), found "
                    "type {}.").format(type(user_data))
            log.error(msg)
            raise TypeError(msg)

        try:
            obj = UserModel._default_manager.get(query)
        except UserModel.DoesNotExist:
            pass

        log.debug("user_data: %s, obj: %s", user_data, obj)
        return obj
