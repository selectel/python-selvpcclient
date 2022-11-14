Command-line Interface
======================

Basic Usage
-----------

In order to use the CLI, you must provide your Selectel VPC API token,
API endpoint and Keystone identity url. Use the corresponding configuration
options (``--url``, ``--token``, ``--identity_url``),
but it is easier to set them in environment variables.

.. code-block:: shell

    export SEL_URL=url
    export SEL_TOKEN=token
    export SEL_API_VERSION=api_version # by default: 2
    export OS_AUTH_URL=url # by default: https://api.selvpc.ru/identity/v3

Once you've configured your authentication parameters, you can run **selvpc**
commands.  All commands take the form of:

.. code-block:: none

    selvpc <command> [arguments...]

Run **selvpc help** to get a full list of all possible commands, and run
**selvpc help <command>** to get detailed help for that command.


Display options
---------------

Filtering
~~~~~~~~~

**selvpc** CLI supports filtering in the listing operation.

To specify a filter in ``* list`` command, you need to pass a pair of an
attribute name and an expected value with the format of ``--<attribute> <value>``.
The example below retrieves subnets added into project.

.. code-block:: console

    $ selvpc subnet list --project xxxx3dc1894748b193031ae1bccf508a
    +-----+----------------------------------+--------+----------------+--------+
    |  id | project_id                       | region | cidr           | status |
    +-----+----------------------------------+--------+----------------+--------+
    | 420 | xxxx3dc1894748b193031ae1bccf508a | ru-1   | xx.xx.xxx.x/29 | DOWN   |
    +-----+----------------------------------+--------+----------------+--------+

You can also specify multiple filters.
The example below retrieves all licenses added into project
locates on ru-2 region

.. code-block:: console

    $ selvpc license list --project xxxx3dc1894748b193031ae1bccf508a --region ru-1
    +-------+----------------------------------+--------+-------------------------------+--------+
    |    id | project_id                       | region | type                          | status |
    +-------+----------------------------------+--------+-------------------------------+--------+
    | xxxxx | xxxx3dc1894748b193031ae1bccf508a | ru-1   | license_windows_2012_standard | DOWN   |
    +-------+----------------------------------+--------+-------------------------------+--------+

Changing displayed columns
~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want displayed columns in a list operation, ``-c`` option can be used.
``-c`` can be specified multiple times and the column order will be same as
the order of ``-c`` options.

.. code-block:: console

    $ selvpc license list -c id
    +-------+
    |    id |
    +-------+
    | xxxxx |
    +-------+


Debugging
---------

Display API-level communication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``-v`` (or ``--verbose``, ``--debug``) option displays a detail interaction
with VPC API. It is useful to debug what happens in the API level.


.. code-block:: console

    found extension EntryPoint.parse('table = cliff.formatters.table:TableFormatter')
    found extension EntryPoint.parse('json = cliff.formatters.json_format:JSONFormatter')
    found extension EntryPoint.parse('csv = cliff.formatters.commaseparated:CSVLister')
    found extension EntryPoint.parse('value = cliff.formatters.value:ValueFormatter')
    found extension EntryPoint.parse('yaml = cliff.formatters.yaml_format:YAMLFormatter')
    REQ: curl -i -XGET "https://api.selectel.ru/vpc/resell/v2/licenses?detailed=False" -H "X-Token: xxx" -H "Content-Type: application/json" -H "Accept: application/json" -H "User-Agent: python-selvpcclient/xxx"
    Starting new HTTPS connection (1): api.selectel.ru
    https://api.selectel.ru:443 "GET /vpc/resell/v2/licenses?detailed=False HTTP/1.1" 200 156
    RESP: 200 {'Content-Length': 'xxx', 'Content-Type': 'application/json', } {"licenses": [{...}]}
    +-------+
    |    id |
    +-------+
    | xxxxx |
    +-------+

Commands
--------

.. toctree::
   :glob:
   :maxdepth: 2

   commands
