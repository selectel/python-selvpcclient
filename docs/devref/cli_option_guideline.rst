CLI Option Guideline
====================

This document describes the conventions of selvpc CLI options.

General conventions
-------------------

#. Option names should be delimited by a hyphen instead of a underscore.
   This is the common guidelines across all OpenStack CLIs.

   * Good: ``--ip-version``
   * Not Good: ``--ip_version``

#. Use at least one required option for ``*-create`` command.  If all options
   are optional, we typically use ``name`` field as a required option.

#. If an attribute name in API is ``foo_id``, the corresponding option
   should be ``--foo`` instead of ``--foo-id``.

   * It is because we usually support ID to specify a resource.

#. Do not use ``nargs='?'`` without a special reason.

   * The behavior of ``nargs='?'`` option for python argparse is
     bit tricky and may lead to unexpected option parsing different
     from the help message. The detail is described in the
     :ref:`Background section <background-nargs>` below.

#. (option) Avoid using positional options as much as possible.

   * Positional arguments should be limited to attributes which will
     be required in the long future.

#. We honor existing options and should keep compatibilities when adding or
   changing options.

Options for boolean value
-------------------------

Use the form of ``--option-name {True|False}``.

* For a new option, it is recommended.
* For existing options, migration to the recommended form is not necessarily
  required. All backward-compatibility should be kept without reasonable
  reasons.

Options for dict value
----------------------

Some API attributes take a dictionary.

``--foo key1=val1,key2=val2`` is usually used.

This means ``{"foo": {"key1": "val1", "key2": "val2"} }`` is passed in the API layer.

Options for list value
----------------------

Some attributes take a list.

In this case, we usually use:

* Define an option per element (Use a singular form as an option name)
* Allow to specify the option multiple times

For Example, **port-create** has ``--security-group`` option.
``selvpc vrrp add XXXX --region ru-1 --region ru-2`` generates
``{"vlan_subnets": {"regions": ["SG1", "SG2"] ... }`` in the API layer.

.. _background-nargs:

Avoid using nargs in positional or optional arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The behavior of ``nargs='?'`` option for python argparse is bit tricky.
When we use ``nargs='?'`` and if the order of command-line options is
changed then the command-line parser may fail to parse the arguments
correctly. Two examples of such failures are provided below.

Example 1:
This example shows how the actual behavior can differ from the provided
help message. In the below block, help message at ``[5]`` says ``--bb CC``
is a valid format but the argument parsing for the same format fails at ``[7]``.

.. code-block:: console

   In [1]: import argparse
   In [2]: parser = argparse.ArgumentParser()
   In [3]: parser.add_argument('--bb', nargs='?')
   In [4]: parser.add_argument('cc')

   In [5]: parser.print_help()
   usage: ipython [-h] [--bb [BB]] cc

   positional arguments:
     cc

   optional arguments:
     -h, --help  show this help message and exit
     --bb [BB]

   In [6]: parser.parse_args('--bb 1 X'.split())
   Out[6]: Namespace(bb='1', cc='X')

   In [7]: parser.parse_args('--bb X'.split())
   usage: ipython [-h] [--bb [BB]] cc
   ipython: error: too few arguments
   An exception has occurred, use %tb to see the full traceback.

   SystemExit: 2


Example 2:
This example shows how fragile ``nargs='?'`` can be when user specifies
options in different order from the help message.

.. code-block:: console

   In [1]: import argparse
   In [2]: parser = argparse.ArgumentParser()
   In [3]: parser.add_argument('--a', help='option a')
   In [4]: parser.add_argument('--b', help='option b')
   In [5]: parser.add_argument('x', help='positional arg X')
   In [6]: parser.add_argument('y', nargs='?', help='positional arg Y')
   In [7]: parser.print_help()
   usage: ipython [-h] [--a A] [--b B] x [y]

   positional arguments:
     x           positional arg X
     y           positional arg Y

   optional arguments:
     -h, --help  show this help message and exit
     --a A       option a
     --b B       option b

   In [8]: parser.parse_args('--a 1 --b 2 X Y'.split())
   Out[8]: Namespace(a='1', b='2', x='X', y='Y')

   In [9]: parser.parse_args('X Y --a 1 --b 2'.split())
   Out[9]: Namespace(a='1', b='2', x='X', y='Y')

   In [10]: parser.parse_args('X --a 1 --b 2 Y'.split())
   usage: ipython [-h] [--a A] [--b B] x [y]
   ipython: error: unrecognized arguments: Y
   An exception has occurred, use %tb to see the full traceback.

   SystemExit: 2

   To exit: use 'exit', 'quit', or Ctrl-D.
   To exit: use 'exit', 'quit', or Ctrl-D.

Note: Most CLI users don't care about the order of the command-line
options. Hence, such fragile behavior should be avoided.
