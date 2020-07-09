import logging

from selvpcclient import base
from selvpcclient.util import resource_filter
from selvpcclient.exceptions.base import ClientException

log = logging.getLogger(__name__)


class VRRP(base.Resource):
    """Represents a vrrp."""

    def delete(self):
        """Delete current vrrp subnet from domain."""
        self.manager.delete(self.id)


class VRRPManager(base.Manager):
    """Manager class for manipulating vrrp subnets."""
    resource_class = VRRP

    @resource_filter
    def list(self, return_raw=False):
        """Get list of all vrrp in current domain.

        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: list of :class:`VRRP`
        """
        return self._list('/vrrp_subnets', 'vrrp_subnets',
                          return_raw=return_raw)

    def add(self, project_id, vrrp, return_raw=False):
        """Create vrrp in project.

        :param string project_id: Project id.
        :param dict vrrp: Dict with key `vrrp` and value as array
                                 of items region and quantity::

                                    {
                                        "vrrp_subnets": [
                                            {
                                                "regions": [
                                                    "master": "ru-1",
                                                    "slave": "ru-2"
                                                ],
                                                "quantity": 1,
                                                "prefix_length": 29,
                                                "type": "ipv4",
                                            }
                                        ]
                                    }
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: list of :class:`VRRP`
        """

        url = '/vrrp_subnets/projects/{}'.format(project_id)
        return self._list(url, 'vrrp_subnets', body=vrrp,
                          return_raw=return_raw)

    def show(self, vrrp_id, return_raw=False):
        """Show detailed vrrp information.

        :param string vrrp_id: VRRP id.
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: :class:`VRRP`
        """
        return self._get('/vrrp_subnets/{}'.format(vrrp_id), 'vrrp_subnet',
                         return_raw=return_raw)

    def delete(self, vrrp_id):
        """Delete vrrp from domain.

        :param string vrrp_id: VRRP id.
        """
        self._delete('/vrrp_subnets/{}'.format(vrrp_id))

    def delete_many(self, vrrp_ids, raise_if_not_found=True):
        """Delete few vrrp subnets from domain.

        :param list vrrp_ids: VRRP subnet id's list
        :param bool raise_if_not_found: Raise exception if object won't found
        """
        for vrrp_id in vrrp_ids:
            try:
                self.delete(vrrp_id)
                log.info("VRRP subnet %s has been deleted", vrrp_id)
            except ClientException as err:
                if raise_if_not_found:
                    raise err
                log.error("%s %s", err, vrrp_id)
