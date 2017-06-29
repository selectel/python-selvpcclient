from selvpcclient import base
from selvpcclient.util import resource_filter


class Subnet(base.Resource):
    """Represents a subnet."""

    def delete(self):
        """Delete current subnet from domain."""
        self.manager.delete(self.id)


class SubnetManager(base.Manager):
    """Manager class for manipulating subnet."""
    resource_class = Subnet

    @resource_filter
    def list(self, detailed=False):
        """Get list of all public subnets in current domain.

        :param bool detailed: Include info about servers. (optional)
        :rtype: list of :class:`Subnet`
        """
        return self._list('/subnets?detailed=' + str(detailed), 'subnets')

    def add(self, project_id, subnets):
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
        :rtype: list of :class:`Subnet`
        """
        url = '/subnets/projects/{}'.format(project_id)
        return self._list(url, 'subnets', body=subnets)

    def show(self, subnet_id):
        """Show detailed subnet information.

        :param string subnet_id: Subnet id.
        :rtype: :class:`Subnet`
        """
        return self._get('/subnets/{}'.format(subnet_id), 'subnet')

    def delete(self, subnet_id):
        """Delete subnet from domain."""
        self._delete('/subnets/{}'.format(subnet_id))
