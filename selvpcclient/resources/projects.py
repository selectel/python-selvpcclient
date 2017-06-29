from selvpcclient import base
from selvpcclient.resources.floatingips import FloatingIPManager
from selvpcclient.resources.licenses import LicenseManager
from selvpcclient.resources.quotas import QuotasManager
from selvpcclient.resources.roles import RolesManager
from selvpcclient.resources.subnets import SubnetManager
from selvpcclient.resources.tokens import TokensManager


class Project(base.Resource):
    """Represents a project."""

    def get(self):
        """Get full information about current project.

        :rtype: :class:`Project` with additional fields.
        """
        return self.manager.get(self.id)

    def update(self, name=None):
        """Update current project properties.

        :param string name: New name for project.
        :rtype: :class:`Project` with new name.
        """
        return self.manager.update(self.id, name or self.name)

    def get_roles(self):
        """List all roles for the project.

        :rtype: list of :class:`selvpcclient.resources.roles.Role`
        """
        return self.manager.roles_manager.get_project_roles(self.id)

    def get_quotas(self):
        """Show quotas info for current project.

        :rtype: list of :class:`selvpcclient.resources.quotas.Quotas`
        """
        return self.manager.quotas_manager.get_project_quotas(
            project_id=self.id)

    def add_license(self, licenses):
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
        :rtype: list of :class:`selvpcclient.resources.licenses.License`
        """
        return self.manager.licenses_manager.add(self.id, licenses)

    def add_subnet(self, subnets):
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
        :rtype: list of :class:`selvpcclient.resources.subnets.Subnet`
        """
        return self.manager.subnets_manager.add(self.id, subnets)

    def add_floating_ips(self, floatingips):
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
        :rtype: list of :class:`selvpcclient.resources.floatingips.FloatingIP`
        """
        return self.manager.fips_manager.add(self.id, floatingips)

    def add_token(self):
        """Create reseller token for current project.

        :rtype: :class:`selvpcclient.resources.tokens.Token`
        """
        return self.manager.token_manager.create(self.id)

    def update_quotas(self, quotas):
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
        :rtype: list of :class:`selvpcclient.resources.quotas.Quotas`
        """
        return self.manager.quotas_manager.update(
            project_id=self.id, quotas=quotas)

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

    def list(self):
        """Get list of projects in current domain.

        :rtype: list of :class:`Project`
        """
        return self._list('/projects', 'projects')

    def create(self, name, quotas=None):
        """Create new project and optionally set quotas on it.

        :param string name: Name of project.
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
        return self._post('/projects', body, 'project')

    def show(self, project_id):
        """Show detailed project information.

        :param string project_id: Project id.
        :rtype: :class:`Project` with additional fields.
        """
        return self._get('/projects/{}'.format(project_id), 'project')

    def update(self, project_id, name):
        """Update Project's properties.

        :param string project_id: Project id.
        :param string name: New name for project.
        :rtype: :class:`Project`
        """

        body = {"project": {"name": name}}
        return self._patch('/projects/{}'.format(project_id), body, 'project')

    def delete(self, project_id):
        """Delete Project and all it's objects.

        :param string project_id: Project id."""
        self._delete('/projects/{}'.format(project_id))
