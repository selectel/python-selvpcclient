from selvpcclient import base
from selvpcclient.util import resource_filter


class FloatingIP(base.Resource):
    """Represents a floating ip."""

    def delete(self):
        """Delete current floatingip from domain."""
        self.manager.delete(self.id)


class FloatingIPManager(base.Manager):
    """Manager class for manipulating floating ip."""
    resource_class = FloatingIP

    @resource_filter
    def list(self, detailed=False):
        """Get list of all floatingips in current domain.

        :param bool detailed: Include info about servers. (optional)
        :rtype: list of :class:`FloatingIP`
        """
        return self._list('/floatingips?detailed=' + str(detailed),
                          'floatingips')

    def add(self, project_id, floatingips):
        """Create floatingips in project.

        :param string project_id: Project id.
        :param dict floatingips: Dict with key `floatingips` and value as array
                                 of items region and quantity::

                                    {
                                        "floatingips": [
                                            {
                                                "region": "ru-1",
                                                "quantity": 4
                                            }
                                        ]
                                    }
        :rtype: list of :class:`FloatingIP`
        """

        url = '/floatingips/projects/{}'.format(project_id)
        return self._list(url, 'floatingips', body=floatingips)

    def show(self, floatingip_id):
        """ Show detailed floatingip information.

        :param string floatingip_id: Floatingip id.
        :rtype: :class:`FloatingIP`
        """
        return self._get('/floatingips/{}'.format(floatingip_id), 'floatingip')

    def delete(self, floatingip_id):
        """Delete floatingip from domain.

        :param string floatingip_id: Floating ip id.
        """
        self._delete('/floatingips/{}'.format(floatingip_id))
