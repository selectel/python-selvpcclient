Python library
==============

Basic Usage
-----------

First create a Client instance using a HttpClient with your api token and actual API URL.
(you might get API token `here <http://support.selectel.ru/keys>`_ and
API URL `here <https://support.selectel.ru/vpc/docs/>`_)

.. code-block:: python

    >>> from selvpcclient.client import Client, setup_http_client
    >>> SEL_TOKEN=YOUR_API_TOKEN_HERE
    >>> SEL_URL="https://api.selectel.ru/vpc/resell"
    >>> http_client = setup_http_client(api_url=SEL_URL, api_token=SEL_TOKEN)
    >>> selvpc = Client(client=http_client)

Now you can call various methods on the client instance. For example

Create a project
~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> project = selvpc.projects.add(name="Bonnie")

Set project quotas
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> quotas = {
        "quotas": {
            "compute_cores": [
                {
                    "region": "ru-1",
                    "zone": "ru-1a",
                    "value": 10
                }
            ],
            "compute_ram": [
                {
                    "region": "ru-1",
                    "zone": "ru-1a",
                    "value": 1024
                }
            ]
        }
    }

    # via object
    >>> project.update_quotas(quotas)

    # via quotas manager
    >>> quotas = selvpc.quotas.update(project.id, quotas=quotas)


Add Windows license
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> licenses = {
      "licenses": [{
          "region": "ru-1",
          "quantity": 1,
          "type": "license_windows_2012_standard"
      }]
    }

    # via object
    >>> project.add_license(license)

    # via licenses manager
    >>> licenses = selvpc.licenses.add(project.id, licenses=licenses)


All available managers
----------------------

Manage Projects
~~~~~~~~~~~~~~~

.. automodule:: selvpcclient.resources.projects
  :members:
  :show-inheritance:


Manage Quotas
~~~~~~~~~~~~~

.. automodule:: selvpcclient.resources.quotas
    :members:
    :show-inheritance:

Manage Licenses
~~~~~~~~~~~~~~~

.. automodule:: selvpcclient.resources.licenses
    :members:
    :show-inheritance:

Manage Users
~~~~~~~~~~~~

.. automodule:: selvpcclient.resources.users
    :members:
    :show-inheritance:

Manage Roles in projects
~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: selvpcclient.resources.roles
    :members:
    :show-inheritance:

Manage Subnets
~~~~~~~~~~~~~~

.. automodule:: selvpcclient.resources.subnets
    :members:
    :show-inheritance:

Manage VRRP Subnets
~~~~~~~~~~~~~~~~~~~

.. automodule:: selvpcclient.resources.vrrp
    :members:
    :show-inheritance:

Manage Floating IP
~~~~~~~~~~~~~~~~~~

.. automodule:: selvpcclient.resources.floatingips
    :members:
    :show-inheritance:

Manage Tokens
~~~~~~~~~~~~~

.. automodule:: selvpcclient.resources.tokens
    :members:
    :show-inheritance: