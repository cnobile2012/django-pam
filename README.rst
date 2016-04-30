==========
Django PAM
==========

.. image:: http://img.shields.io/pypi/v/django-pam.svg
   :target: https://pypi.python.org/pypi/django-pam
   :alt: PyPI Version

.. image:: http://img.shields.io/travis/cnobile/django-pam/master.svg
   :target: http://travis-ci.org/cnobile/django-pam
   :alt: Build Status

.. image:: http://img.shields.io/coveralls/cnobile/django-pam/master.svg
   :target: https://coveralls.io/r/cnobile/django-pam
   :alt: Test Coverage

A Django PAM authentication backend implementation.

The MIT License (MIT)

Overview
========

This is a simple backend that uses the *python-pam* package found at
https://github.com/FirefighterBlu3/python-pam. It can be used in a SSO
(Single Sign On) environment or just on a single box where you want to
log into a Django app with the UNIX login.

Direction I hope to take with this project.
===========================================

 1. A Django authentication backend plugin.
 2. Login and Logout views.
