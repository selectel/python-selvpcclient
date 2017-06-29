from selvpcclient import base
from selvpcclient.util import resource_filter


class VRRP(base.Resource):
    """Represents a vrrp."""

    def delete(self):
        """Delete current vrrp subnet from domain."""
        self.manager.delete(self.id)


class VRRPManager(base.Manager):
    """Manager class for manipulating vrrp subnets."""
    resource_class = VRRP

    @resource_filter
    def list(self):
        """Get list of all vrrp in current domain.

        :rtype: list of :class:`VRRP`
        """
        return self._list('/vrrp_subnets', 'vrrp_subnets')

    def add(self, project_id, vrrp):
        """Create vrrp in project.

        :param string project_id: Project id.
        :param dict vrrp: Dict with key `vrrp` and value as array
                                 of items region and quantity::

                                    {
                                        "vrrp_subnets": [
                                            {
                                                "regions": ["ru-1", "ru-2"],
                                                "quantity": 1,
                                                "prefix_length": 29,
                                                "type": "ipv4",
                                            }
                                        ]
                                    }
        :rtype: list of :class:`VRRP`
        """

        url = '/vrrp_subnets/projects/{}'.format(project_id)
        return self._list(url, 'vrrp_subnets', body=vrrp)

    def show(self, vrrp_id):
        """Show detailed vrrp information.

        :param string vrrp_id: VRRP id.
        :rtype: :class:`VRRP`
        """
        return self._get('/vrrp_subnets/{}'.format(vrrp_id), 'vrrp_subnet')

    def delete(self, vrrp_id):
        """Delete vrrp from domain.

        :param string vrrp_id: VRRP id.
        """
        self._delete('/vrrp_subnets/{}'.format(vrrp_id))
