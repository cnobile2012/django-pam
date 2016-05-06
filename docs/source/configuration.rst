Configuration
*************

Installing the Backend Authenticator
====================================

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

.. note::

  1. The user that runs the application needs to be a member of the
     ``/etc/shadow`` file group. This is necessary so the user can
     authenticate other users.
       ``sudo usermod -a -G shadow <user>``

  2. If you use your UNIX account username you will be logged in through
     the ``PAMBackend`` backend. If you use the Django username you will
     be logged in through the ``ModelBackend``, assuming  both usernames
     and passwords are not the same.

Using the Django PAM Login and Logout Templates
===============================================

Use as is with Django PAM CSS
-----------------------------

Add the statement below to your ``urls.py`` files::

  url(r'^django-pam/', include('django_pam.urls')),

Then put the HTML below in your template::

  {% load staticfiles %}
  <a href="{% url 'django-pam:login' %}">Login</a>
  <a href="{% url 'django-pam:logout' %}?next={{ next }}">Logout</a>

Use Modified CSS
----------------

Add the statements below to your ``urls.py`` files::

  url(r'^login/$', LoginView.as_view(template_name='home/login.html'),
      name='login'),
  url(r"^logout/(?P<next>[\w\-\:/]+)?$", LogoutView.as_view(
      template_name='home/logout.html'), name='logout'),

Create ``login.html`` and ``logout.html`` templates.

Login::

  {% extends "your_base.html" %}
  {% load staticfiles %}
  {% block script %}
      {{ form.media }}
      <link rel="stylesheet" href="{% static '<your css file>' %}">
  {% endblock %}
  {% block content %}{% include "django_pam/accounts/_login.html" %}{% endblock %}

The stanza above includes the Django PAM CSS and JavaScript code
through the form. Then the overriding CSS is included. The JavaScript
code, that's included from the form, is not dependent on any toolkit.

Logout::

  {% extends "your_base.html" %}
  {% load staticfiles %}
  {% block script %}
      <link rel="stylesheet" href="{% static 'django_pam/css/auth.css' %}">
      <link rel="stylesheet" href="{% static '<your css file>' %}">
  {% endblock %}
  {% block content %}{% include "django_pam/accounts/_logout.html" %}{% endblock %}

There is no form for logout so the CSS from Django PAM and the
overriding CSS need to be included the normal way.

Then use something like the HTML below in your HTML template::

  {% load staticfiles %}
  <a href="{% url 'login' %}">Login</a>
  <a href="{% url 'logout' %}?next={{ next }}">Logout</a>

Using the Django PAM Login and Logout Modals
============================================

Using the modals require a little more work, but it's still not to
difficult.

In your ``base.html`` head include::

  <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css"
        type="text/css" media="all" rel="stylesheet" />
  <link href="{% static 'django_pam/css/modal.css' %}" type="text/css"
        media="all" rel="stylesheet" />
  <script src="https://code.jquery.com/jquery-2.2.3.min.js"
          integrity="sha256-a23g1Nt4dtEYOj7bR+vTu7+T8VP13humZFBJNIYoEJo="
          crossorigin="anonymous"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
  <script src="{% static 'django_pam/js/js.cookie-2.0.4.min.js' %}"></script>
  <script src="{% static 'django_pam/js/inheritance.js' %}"></script>
  <script src="{% static 'django_pam/js/modal.js' %}"></script>

At the bottom of your ``base.html`` template include this line just
before the ``</html>`` tag::

  {% block modals %}{% endblock %}

Then in the template that has your login html add at the bottom of the
template::

  {% block modals %}
  <div id="modals">
    {% include "django_pam/modals/login.html" %}
    {% include "django_pam/modals/logout.html" %}
  </div> <!-- div#modals -->
  {% endblock %}

.. note::

  The JavaScript for the modals is written in ES6 which is supported
  in most of the newer browsers. See:
  `ECMAScript 6 <https://github.com/lukehoban/es6features>`_.

  Use `Babel <https://babeljs.io/>`_ or `Traceur
  <https://github.com/google/traceur-compiler>`_ if you wish to
  `Transpile
  <https://en.wikipedia.org/wiki/Source-to-source_compiler>`_  my
  JavaScript code.
