==========
Django PAM
==========

.. image:: http://img.shields.io/pypi/v/django-pam.svg
   :target: https://pypi.python.org/pypi/django-pam
   :alt: PyPI Version

.. image:: http://img.shields.io/travis/cnobile2012/django-pam/master.svg
   :target: http://travis-ci.org/cnobile2012/django-pam
   :alt: Build Status

.. image:: http://img.shields.io/coveralls/cnobile2012/django-pam/master.svg
   :target: https://coveralls.io/r/cnobile2012/django-pam
   :alt: Test Coverage

A Django PAM authentication backend implementation.

The MIT License (MIT)

Overview
--------

This is a simple authentication backend that uses the
`python-pam <https://github.com/FirefighterBlu3/python-pam>`_
package. Django PAM can be used in an SSO (Single Sign On) environment
or just with a single box where you want to log into a Django app with
your UNIX login.

Provides
--------

1. PAM Authentication Backend

2. Login and Logout Views

3. Templates for both standard and modal authentication.

4. Supporting JavaScript and CSS.

Quick Start
-----------

You will need to add Django PAM to your ``INSTALLED_APPS``::

  INSTALLED_APPS = [
      ...
      'django_pam',
  ]

Next you will need to add the Django PAM backend to the
 ``AUTHENTICATION_BACKENDS``::

  AUTHENTICATION_BACKENDS = [
      'django_pam.auth.backends.PAMBackend',
      'django.contrib.auth.backends.ModelBackend',
  ]

Complete Documentation can be found at
`Read the Docs <https://readthedocs.org/>`_  at:
`Django PAM <https://readthedocs.org/projects/django-pam>`_
