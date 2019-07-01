import logging

from selvpcclient import base
from selvpcclient.util import resource_filter
from selvpcclient.exceptions.base import ClientException

log = logging.getLogger(__name__)


class License(base.Resource):
    """Represents a license."""

    def delete(self):
        """Delete current license from domain."""
        self.manager.delete(self.id)


class LicenseManager(base.Manager):
    """Manager class for manipulating licenses."""
    resource_class = License

    @resource_filter
    def list(self, detailed=False, return_raw=False):
        """Get list of all licenses in current domain.

        :param bool detailed: Include info about servers. (optional)
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: list of :class:`License`
        """
        return self._list('/licenses?detailed=' + str(detailed), 'licenses',
                          return_raw=return_raw)

    def add(self, project_id, licenses, return_raw=False):
        """Create licenses for project.

        :param string project_id: Project id.
        :param dict licenses: Dict with key `licenses` and value as array
                              of items region, quantity and type::

                                 {
                                     "licenses": [{
                                        "region": "ru-1",
                                        "quantity": 4,
                                        "type": "license_windows_2012_standard"
                                     },
                                     {
                                        "region": "ru-2",
                                        "quantity": 1,
                                        "type": "license_windows_2012_standard"
                                     }]
                                 }
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: list of :class:`License`
        """
        url = '/licenses/projects/{}'.format(project_id)
        return self._list(url, 'licenses', body=licenses,
                          return_raw=return_raw)

    def show(self, license_id, return_raw=False):
        """ Show detailed license information.

        :param string license_id: License id.
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: :class:`License`
        """
        return self._get('/licenses/{}'.format(license_id),
                         response_key='license',
                         return_raw=return_raw)

    def delete(self, license_id):
        """Delete license from domain.

        :param string license_id: License id.
        """
        self._delete('/licenses/{}'.format(license_id))

    def delete_many(self, license_ids, raise_if_not_found=True):
        """Delete few licenses from domain.

        :param list license_ids: Subnet id's list
        :param bool raise_if_not_found: Raise exception if object won't found
        """
        for license_id in license_ids:
            try:
                self.delete(license_id)
                log.info("License %s has been deleted", license_id)
            except ClientException as err:
                if raise_if_not_found:
                    raise err
                log.error("%s %s", err, license_id)
