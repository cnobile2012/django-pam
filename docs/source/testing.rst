Testing
*******

The `$USER` of the server that runs an application, that uses this backend,
needs to be a member of the UNIX shadow group. This causes testing is a bit
tricky. Because of this, some tests in the test suite remove the `python_pam`
package from tests when run on GitHub. This allows the current maintainer to
test with different versions or Python and run coverage. You can, however, run
tests locally by following a few steps.

Give Your User Account Shadow Privileges
========================================

This assumes that it is your user account that the `runserver` is running in.
If not, then use the account that is running the `runserver`.

.. code-block:: bash

   $ sudo usermod -a -G shadow <username>

Create a `guest` User
=====================

.. code-block:: php

   $ sudo useradd guest -m -s /bin/bash -d /home/guest
   $ sudo passwd guest

You will need to logout of your account then log back in again, this means out
of any GUI that you may be in.

After logged back in tests will run correctly, however, you will need to enter
the username and password multiple times, but this will get old fast, so do
the following.

Creating a `.django_pam` File
=============================

Create a `.django_pam` file in the same directory as `manage.py`. On separate
lines put `guest` (the username), the password you chose for it, and then a
fake email address. Like this:

.. code-block:: php

   <username>
   <password>
   <username>@somesite.com

With this file in-place the tests will run to completion without asking for
the username and password.
