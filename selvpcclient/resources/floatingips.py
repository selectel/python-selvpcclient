import logging

from selvpcclient import base
from selvpcclient.util import resource_filter
from selvpcclient.exceptions.base import ClientException

log = logging.getLogger(__name__)


class FloatingIP(base.Resource):
    """Represents a floating ip."""

    def delete(self):
        """Delete current floating ip from domain."""
        self.manager.delete(self.id)


class FloatingIPManager(base.Manager):
    """Manager class for manipulating floating ip."""
    resource_class = FloatingIP

    @resource_filter
    def list(self, detailed=False, return_raw=False):
        """Get list of all floating ip's in current domain.

        :param bool detailed: Include info about servers. (optional)
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: list of :class:`FloatingIP`
        """
        return self._list('/floatingips?detailed=' + str(detailed),
                          'floatingips', return_raw=return_raw)

    def add(self, project_id, floatingips, return_raw=False):
        """Create floating ip's in project.

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
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: list of :class:`FloatingIP`
        """

        url = '/floatingips/projects/{}'.format(project_id)
        return self._list(url, 'floatingips', body=floatingips,
                          return_raw=return_raw)

    def show(self, floatingip_id, return_raw=False):
        """ Show detailed floating ip information.

        :param string floatingip_id: Floating ip id.
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: :class:`FloatingIP`
        """
        return self._get('/floatingips/{}'.format(floatingip_id), 'floatingip',
                         return_raw=return_raw)

    def delete(self, floatingip_id):
        """Delete floatingip from domain.

        :param string floatingip_id: Floating ip id.
        """
        self._delete('/floatingips/{}'.format(floatingip_id))

    def delete_many(self, floatingip_ids, raise_if_not_found=True):
        """Delete few floating ip's from domain.

        :param list floatingip_ids: Subnet id's list
        :param bool raise_if_not_found: Raise exception if object won't found
        """
        for floatingip_id in floatingip_ids:
            try:
                self.delete(floatingip_id)
                log.info("IP %s has been deleted", floatingip_id)
            except ClientException as err:
                if raise_if_not_found:
                    raise err
                log.error("%s %s", err, floatingip_id)
