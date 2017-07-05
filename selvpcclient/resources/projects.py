from selvpcclient import base
from selvpcclient.resources.floatingips import FloatingIPManager
from selvpcclient.resources.licenses import LicenseManager
from selvpcclient.resources.quotas import QuotasManager
from selvpcclient.resources.roles import RolesManager
from selvpcclient.resources.subnets import SubnetManager
from selvpcclient.resources.tokens import TokensManager


class Project(base.Resource):
    """Represents a project."""

    def get(self, return_raw=False):
        """Get full information about current project.

        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: :class:`Project` with additional fields.
        """
        return self.manager.get(self.id, return_raw=return_raw)

    def update(self, name=None, return_raw=False):
        """Update current project properties.

        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :param string name: New name for project.
        :rtype: :class:`Project` with new name.
        """
        return self.manager.update(self.id, name or self.name,
                                   return_raw=return_raw)

    def get_roles(self, return_raw=False):
        """List all roles for the project.

        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: list of :class:`selvpcclient.resources.roles.Role`
        """
        return self.manager.roles_manager.get_project_roles(
            self.id,
            return_raw=return_raw)

    def get_quotas(self, return_raw=False):
        """Show quotas info for current project.

        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: list of :class:`selvpcclient.resources.quotas.Quotas`
        """
        return self.manager.quotas_manager.get_project_quotas(
            project_id=self.id,
            return_raw=return_raw)

    def add_license(self, licenses, return_raw=False):
        """Create licenses for current project.

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
        :rtype: list of :class:`selvpcclient.resources.licenses.License`
        """
        return self.manager.licenses_manager.add(self.id, licenses,
                                                 return_raw=return_raw)

    def add_subnet(self, subnets, return_raw=False):
        """Add public subnets to current project.

        :param dict subnets: Dict with key `subnets` and value as array
                             of items region, quantity and type::

                                {
                                    "subnets": [
                                        {
                                            "region": "ru-1",
                                            "quantity": 4,
                                            "type": "ipv4"
                                        }
                                    ]
                                }
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: list of :class:`selvpcclient.resources.subnets.Subnet`
        """
        return self.manager.subnets_manager.add(self.id, subnets,
                                                return_raw=return_raw)

    def add_floating_ips(self, floatingips, return_raw=False):
        """Add floatingips to current project.

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
        :rtype: list of :class:`selvpcclient.resources.floatingips.FloatingIP`
        """
        return self.manager.fips_manager.add(self.id, floatingips,
                                             return_raw=return_raw)

    def add_token(self, return_raw=False):
        """Create reseller token for current project.

        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: :class:`selvpcclient.resources.tokens.Token`
        """
        return self.manager.token_manager.create(self.id,
                                                 return_raw=return_raw)

    def update_quotas(self, quotas, return_raw=False):
        """Update current project's quotas.

        :param dict quotas: Dict with key `quotas` and keys as dict
                            of items region, zone and value::

                                {
                                    "quotas": {
                                        "compute_cores": [
                                            {
                                                "region": "ru-1",
                                                "zone": "ru-1a",
                                                "value": 10
                                            },
                                            {
                                                "region": "ru-1",
                                                "zone": "ru-1b",
                                                "value": 10
                                            }
                                        ]
                                    }
                                }
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: list of :class:`selvpcclient.resources.quotas.Quotas`
        """
        return self.manager.quotas_manager.update(project_id=self.id,
                                                  quotas=quotas,
                                                  return_raw=return_raw)

    def delete(self):
        """Delete current project and all it's objects."""
        return self.manager.delete(self.id)


class ProjectsManager(base.Manager):
    """Manager class for manipulating project."""
    resource_class = Project

    def __init__(self, client):
        super(ProjectsManager, self).__init__(client)
        self.roles_manager = RolesManager(client)
        self.quotas_manager = QuotasManager(client)
        self.licenses_manager = LicenseManager(client)
        self.token_manager = TokensManager(client)
        self.subnets_manager = SubnetManager(client)
        self.fips_manager = FloatingIPManager(client)

    def list(self, return_raw=False):
        """Get list of projects in current domain.

        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: list of :class:`Project`
        """
        return self._list('/projects', 'projects', return_raw=return_raw)

    def create(self, name, quotas=None, return_raw=False):
        """Create new project and optionally set quotas on it.

        :param string name: Name of project.
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :param dict quotas: Dict with key `quotas` and keys as dict
                            of items region, zone and value::

                                {
                                    "quotas": {
                                        "compute_cores": [
                                            {
                                                "region": "ru-1",
                                                "zone": "ru-1a",
                                                "value": 10
                                            },
                                            {
                                                "region": "ru-1",
                                                "zone": "ru-1b",
                                                "value": 10
                                            }
                                        ]
                                    }
                                }
        :rtype: list of :class:`Project`.
        """
        body = {"project": {"name": name}}
        if quotas:
            body["project"]["quotas"] = quotas
        return self._post('/projects', body, 'project', return_raw=return_raw)

    def show(self, project_id, return_raw=False):
        """Show detailed project information.

        :param string project_id: Project id.
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: :class:`Project` with additional fields.
        """
        return self._get('/projects/{}'.format(project_id), 'project',
                         return_raw=return_raw)

    def update(self, project_id, name=None, return_raw=False):
        """Update Project's properties.

        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :param string project_id: Project id.
        :param string name: New name for project.
        :rtype: :class:`Project`
        """
        body = {"project": {"name": name}}
        return self._patch('/projects/{}'.format(project_id), body, 'project',
                           return_raw=return_raw)

    def delete(self, project_id):
        """Delete Project and all it's objects.

        :param string project_id: Project id."""
        self._delete('/projects/{}'.format(project_id))
