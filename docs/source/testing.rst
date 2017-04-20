Testing
*******

Since the user of the server that runs an application, that uses the backend
provided by this package, needs to be a member of the UNIX shadow group,
testing is a bit complicated. Because of this, this project is not able to run
on `Travis CI <https://travis-ci.org>`_. However, setting up tests to run
locally can be done by following the few steps.

Give Your User Account Shadow Privileges
========================================

This assumes that it is your user account that the `runserver` is running in.
If not, then use the account that is running the `runserver`.

.. code-block:: bash

   $ sudo usermod -a -G shadow <username>

Create a `guest` User
=====================

.. code-block:: bash

   $ sudo useradd guest -m -s /bin/bash -d /home/guest
   $ sudo passwd guest

You will need to logout of your account then log back in again, this means out
of any GUI that you may be in.

After logged back in tests will run correctly, however, you will need to enter
the username and password multiple times. This will get old fast.

Creating a `.django_pam` File
=============================

Create a `.django_pam` file in the same directory as `manage.py`. On separate
lines put `guest` (the username), the password you chose for it, and then a
fake email address.

With this file in-place the test will no longer prompt for the username and
password and will run all the tests with no prompts.
