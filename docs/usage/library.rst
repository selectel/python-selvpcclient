Python library
==============

Basic Usage
-----------

First create a Client instance using a HttpClient with your api token and actual API URL.
(you might get API token `here <http://support.selectel.ru/keys>`_ and
API URL `here <https://support.selectel.ru/vpc/docs/>`_)

.. code-block:: python

    >>> from selvpcclient.client import Client
    >>> from selvpcclient.client import setup_http_client
    >>> from selvpcclient.httpclient import RegionalHTTPClient

    >>> SEL_TOKEN = YOUR_API_TOKEN_HERE
    >>> SEL_URL = "https://api.selectel.ru/vpc/resell"
    >>> OS_AUTH_URL = "https://api.selvpc.ru/identity/v3"

    >>> http_client = setup_http_client(
    ...     api_url=SEL_URL, api_token=SEL_TOKEN)

    >>> regional_http_client = RegionalHTTPClient(
    ...     http_client=http_client,
    ...     identity_url=OS_AUTH_URL)

    >>> selvpc = Client(client=http_client, regional_client=regional_http_client)

Now you can call various methods on the client instance. For example

Create a project
~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> project = selvpc.projects.create("Bonnie")

Also you can get raw json from VPC API by passing **return_raw=True** param.
It's suitable for all managers' methods that return values.

.. code-block:: python

    >>> project_json = selvpc.projects.create("Clyde", return_raw=True)
    >>> project_json
     {
        "name": "Clyde",
        "id": "996b3a5f12c341feb41ddf4c1980371c",
        "url": "https://50377.selvpc.ru",
        "enabled": True
     }

Set project quotas
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> quotas = {
        "quotas": {
            "compute_cores": [
                {
                    "zone": "ru-1a",
                    "value": 10
                }
            ],
            "compute_ram": [
                {
                    "zone": "ru-1a",
                    "value": 1024
                }
            ]
        }
    }

    # via object
    >>> project.update_quotas("ru-1", quotas)

    # via quotas manager
    >>> quotas = selvpc.quotas.update_project_quotas(project.id, "ru-1", quotas)

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


Delete objects
~~~~~~~~~~~~~~
It's possible to delete few object at once. Key **raise_if_not_found** will raise an exception
and deleting will be break. (by default **raise_if_not_found**=True)

.. code-block:: python

    >> selvpc.projects.delete_many(project_ids=["58e86b871f474fe2bb2874f9df1a0938",
                                                "58e86b871f474fe2bb2874f9df1a0939",
                                                "58e86b871f474fe2bb2874f9df1a0910"],
                                                raise_if_not_found=False)

      Project 58e86b871f474fe2bb2874f9df1a0938 has been deleted
      Project 58e86b871f474fe2bb2874f9df1a0939 has been deleted
      Project not found 58e86b871f474fe2bb2874f9df1a0910

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

Manage Keypairs
~~~~~~~~~~~~~~~

.. automodule:: selvpcclient.resources.keypairs
    :members:
    :show-inheritance:
