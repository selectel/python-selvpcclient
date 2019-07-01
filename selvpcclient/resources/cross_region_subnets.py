import logging

from selvpcclient import base
from selvpcclient.util import resource_filter
from selvpcclient.exceptions.base import ClientException

log = logging.getLogger(__name__)


class CrossRegionSubnet(base.Resource):
    """Represents a cross-region subnet."""

    def delete(self):
        """Delete current cross-region subnet from domain."""
        self.manager.delete(self.id)


class CrossRegionSubnetManager(base.Manager):
    """Manager class for manipulating cross-region subnets."""
    resource_class = CrossRegionSubnet

    @resource_filter
    def list(self, detailed=False, return_raw=False):
        """Get list of all cross-region subnets in current domain.

        :param bool detailed: Include info about servers. (optional)
        :param bool return_raw: Flag to force returning raw JSON instead of
                                Python object of self.resource_class.
        :rtype: list of :class:`CrossRegionSubnet`.
        """
        return self._list('/cross_region_subnets?detailed=' + str(detailed),
                          'cross_region_subnets', return_raw=return_raw)

    def add(self, project_id, cross_region_subnets, return_raw=False):
        """Create cross-region subnets in project.

        :param string project_id: Project ID.
        :param dict cross_region_subnets: Dict with key `cross_region_subnets`
                                          and value as array of items regions,
                                          CIDR and quantity:

                                          {
                                              "cross_region_subnets": [
                                                   {
                                                       "quantity": 2,
                                                       "regions": [
                                                           {"region": "ru-1"},
                                                           {"region": "ru-2"}
                                                        ]
                                                       "cidr": "192.168.1.0/24"
                                                  }
                                              ]
                                          }
        :param return_raw: flag to force returning raw JSON instead of
                           Python object of self.resource_class.
        :rtype: list of :class:`CrossRegionSubnet`.
        """
        url = '/cross_region_subnets/projects/{}'.format(project_id)
        return self._list(url, 'cross_region_subnets',
                          body=cross_region_subnets,
                          return_raw=return_raw)

    def show(self, cross_region_subnet_id, return_raw=False):
        """Show detailed cross-region information.

        :param string cross_region_subnet_id: Cross-region subnet ID.
        :param return_raw: flag to force returning raw JSON instead of
                           Python object of self.resource_class.
        :rtype: :class:`CrossRegionSubnet`.
        """
        return self._get(
            '/cross_region_subnets/{}'.format(cross_region_subnet_id),
            'cross_region_subnet', return_raw=return_raw)

    def delete(self, cross_region_subnet_id):
        """Delete cross-region subnet.

        :param string cross_region_subnet_id: Cross-region subnet ID.
        """
        self._delete('/cross_region_subnets/{}'.format(cross_region_subnet_id))

    def delete_many(self, cross_region_subnet_ids, raise_if_not_found=True):
        """Delete few cross-region subnets.

        :param list cross_region_subnet_ids: List of cross-region subnets IDs.
        :param bool raise_if_not_found: Raise exception if object wasn't found.
        """
        for cross_region_subnet_id in cross_region_subnet_ids:
            try:
                self.delete(cross_region_subnet_id)
                log.info("Cross-region subnet %s has been deleted",
                         cross_region_subnet_id)
            except ClientException as err:
                log.error("%s %s", err, cross_region_subnet_id)
                if raise_if_not_found:
                    raise err
