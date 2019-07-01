import logging

from selvpcclient import base
from selvpcclient.util import resource_filter
from selvpcclient.exceptions.base import ClientException

log = logging.getLogger(__name__)


class Subnet(base.Resource):
    """Represents a subnet."""

    def delete(self):
        """Delete current subnet from domain."""
        self.manager.delete(self.id)


class SubnetManager(base.Manager):
    """Manager class for manipulating subnet."""
    resource_class = Subnet

    @resource_filter
    def list(self, detailed=False, return_raw=False):
        """Get list of all public subnets in current domain.

        :param bool detailed: Include info about servers. (optional)
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: list of :class:`Subnet`
        """
        return self._list('/subnets?detailed=' + str(detailed), 'subnets',
                          return_raw=return_raw)

    def add(self, project_id, subnets, return_raw=False):
        """Create public subnets for project.

        :param string project_id: Project id.
        :param dict subnets: Dict with key `subnets` and value as array
                             of items region, quantity and type::

                                {
                                    "subnets": [
                                        {
                                            "region": "ru-1",
                                            "quantity": 4,
                                            "type": "ipv4",
                                            "prefix_length": 29
                                        }
                                    ]
                                }
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: list of :class:`Subnet`
        """
        url = '/subnets/projects/{}'.format(project_id)
        return self._list(url, 'subnets', body=subnets, return_raw=return_raw)

    def show(self, subnet_id, return_raw=False):
        """Show detailed subnet information.

        :param string subnet_id: Subnet id.
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: :class:`Subnet`
        """
        return self._get('/subnets/{}'.format(subnet_id), 'subnet',
                         return_raw=return_raw)

    def delete(self, subnet_id):
        """Delete subnet from domain."""
        self._delete('/subnets/{}'.format(subnet_id))

    def delete_many(self, subnet_ids, raise_if_not_found=True):
        """Delete few subnets from domain.

        :param list subnet_ids: Subnet id's list
        :param bool raise_if_not_found: Raise exception if object won't found
        """

        for subnet_id in subnet_ids:
            try:
                self.delete(subnet_id)
                log.info("Subnet %s has been deleted", subnet_id)
            except ClientException as err:
                if raise_if_not_found:
                    raise err
                log.error("%s %s", err, subnet_id)
