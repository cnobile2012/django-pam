Overview
********

Backend Authenticator
=====================

PAMBackend.authenticate Authentication method [#f1]_
  This method has two keyword arguments one for the username and the
  other for the password, both are manditory. There is a third
  argument used to pass in a dict of additional arguments that you may
  want stored in the database on the first login of the user.

  In order to use the additional arguments both the
  ``django.contrib.auth.authenticate`` function and either the
  ``django.contrib.auth.forms.AuthenticationForm`` or the Django PAM
  ``django_pam.accounts.forms.AuthenticationForm`` would need to be
  overridden, depending on which one you use.

PAMBackend.get_user Returns the authenticated user [#f2]_
  There is one positional argument that can be the ``pk``,
  ``username``, or ``email``. The ``email`` would be used only if the
  ``email`` is used instead of the ``username`` to identify the user.

Login and Logout Views
======================

LoginView [#f3]_
----------------

Usage::

  url(r'^login/$', LoginView.as_view(
      form_class=MyAuthenticationForm,
      success_url='/my/success/url/',
      redirect_field_name='my-redirect-field-name',
      template_name='your_template.html'
      ), name='login'),

This view is written to work with either a template *POST* or a
*XMLHttpRequest POST* request.

LogoutView [#f4]_
-----------------

Usage::

  url(r'^logout/$', LogoutView.as_view(
      template_name='my_template.html',
      success_url='/my/success/url/),
      redirect_field_name='my-redirect-field-name'
      ), name='logout')

This view is written to work with either a template *POST* or a
*XMLHttpRequest POST* request.

.. rubric:: Footnotes

.. [#f1] See source :py:meth:`django_pam.auth.backends.PAMBackend.authenticate`
.. [#f2] See source :py:meth:`django_pam.auth.backends.PAMBackend.get_user`
.. [#f3] See source :py:class:`django_pam.accounts.views.LoginView`
.. [#f4] See source :py:class:`django_pam.accounts.views.LogoutView`
