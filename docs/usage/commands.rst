Show capabilities
~~~~~~~~~~~~~~~~~
.. code-block:: console

   $ selvpc capabilities show regions
   $ selvpc capabilities show licenses
   $ selvpc capabilities show traffic
   $ selvpc capabilities show resources
   $ selvpc capabilities show subnets

Manage customization
~~~~~~~~~~~~~~~~~~~~
.. code-block:: console
   $ selvpc customization update [--logo VALUE] [--color COLOR]
   $ selvpc customization show
   $ selvpc customization delete --yes-i-really-want-to-delete

.. note::
   The key **--yes-i-really-want-to-delete** is required always.

.. note::
   **--logo** param can be like URL to logo or local path.


Show domain limits
~~~~~~~~~~~~~~~~~~
.. code-block:: console

   $ selvpc limit show
   $ selvpc limit show free

Manage projects
~~~~~~~~~~~~~~~
.. code-block:: console

   $ selvpc project list
   $ selvpc project create --name VALUE
   $ selvpc project show <project_id>
   $ selvpc project update <project_id> [--name VALUE] [--logo VALUE] [--color VALUE] [--reset-logo] [--reset-color]
   [--reset-theme] [--reset-cname]
   $ selvpc project delete <project_id> --yes-i-really-want-to-delete

.. note::
   The key **--yes-i-really-want-to-delete** is required always.

.. note::
   **--logo** param can be like URL to logo or local path.

.. note::
   **--reset-theme** flag equals to **--reset-logo** and **--reset-color** together.

Manage quotas
~~~~~~~~~~~~~
.. code-block:: console

   $ selvpc quota list
   $ selvpc quota optimize <project_id>
   $ selvpc quota show <project_id>
   $ selvpc quota set <project_id> --resource VALUE --region VALUE [--zone VALUE] --value VALUE

.. note::
   Key **zone** by default is empty.

Manage users
~~~~~~~~~~~~
.. code-block:: console

   $ selvpc user list
   $ selvpc user roles <user_id>
   $ selvpc user create --name VALUE --password VALUE [--enabled VALUE]
   $ selvpc user update <user_id> --name VALUE --password VALUE --enabled VALUE
   $ selvpc user delete <user_id> --yes-i-really-want-to-delete

.. note::
   If you want to update some property, such as a password, you do not need to specify all fields like name or enabled. Suffice it **user_id** and **password**

.. note::
   Key **enabled** by default is **True**.

Manage roles
~~~~~~~~~~~~
.. code-block:: console

   $ selvpc role list <project_id>
   $ selvpc role create --project_id VALUE --user_id VALUE
   $ selvpc role delete --project_id VALUE --user_id VALUE

Manage licenses
~~~~~~~~~~~~~~~
.. code-block:: console

   $ selvpc license list [--detailed]
   $ selvpc license show <license_id>
   $ selvpc license add <project_id> --region VALUE --type VALUE [--quantity VALUE]
   $ selvpc license delete <license_id> --yes-i-really-want-to-delete

.. note::
   The key **--detailed** show addictional columns like a servers.

.. note::
   Key **quantity** by default is **1**

Manage floating ips
~~~~~~~~~~~~~~~~~~~
.. code-block:: console

   $ selvpc floating list [--detailed]
   $ selvpc floating show <floatingip_id>
   $ selvpc floating add <project_id> --region VALUE [--quantity VALUE]
   $ selvpc floating delete <floatingip_id> --yes-i-really-want-to-delete

.. note::
   The key **--detailed** show addictional columns like a servers.

.. note::
   Key **quantity** by default is **1**

Manage subnets
~~~~~~~~~~~~~~
.. code-block:: console

   $ selvpc subnet list [--detailed]
   $ selvpc subnet show <subnet_id>
   $ selvpc subnet add <project_id> --region VALUE [--type VALUE] [--prefix VALUE] [--quantity VALUE]
   $ selvpc subnet delete <subnet_id> --yes-i-really-want-to-delete

.. note::
   The key **--detailed** show addictional columns like a network_id and servers.

.. note::
   By defaults: key **type** is **ipv4**, **prefix** is **29**, **quantity** is **1**

Manage VRRP subnets
~~~~~~~~~~~~~~~~~~~
.. code-block:: console

   selvpc vrrp add --region ru-1 --region ru-2 [--type VALUE] [--prefix VALUE] [--quantity VALUE]
   selvpc vrrp list [--project XXX] [--detailed]
   selvpc vrrp show 9
   selvpc vrrp delete 9 --yes-i-really-want-to-delete

.. note::
   Key **detailed** appends additional column: *servers*.

.. note::
   Key **region** is repeatable.

.. note::
   By defaults: key **type** is **ipv4**, **prefix** is **29**, **quantity** is **1**

Manage tokens
~~~~~~~~~~~~~
.. code-block:: console

   $ selvpc token create <project_id>