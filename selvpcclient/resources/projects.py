import logging
from typing import Union

from selvpcclient import base
from selvpcclient.base import PartialResponse
from selvpcclient.exceptions.base import ClientException
from selvpcclient.resources.floatingips import FloatingIPManager
from selvpcclient.resources.licenses import LicenseManager
from selvpcclient.resources.quotas import Quotas
from selvpcclient.resources.quotas import QuotasManager
from selvpcclient.resources.roles import RolesManager
from selvpcclient.resources.subnets import SubnetManager
from selvpcclient.resources.tokens import TokensManager
from selvpcclient.util import process_theme_params

log = logging.getLogger(__name__)


class Project(base.Resource):
    """Represents a project."""

    def get(self, return_raw=False):
        """Get full information about current project.

        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: :class:`Project` with additional fields.
        """
        return self.manager.get(self.id, return_raw=return_raw)

    def update(self, name=None, cname=None, color=None, brand_color=None,
               logo=None, reset_cname=False, reset_color=False,
               reset_logo=False, reset_theme=False,
               return_raw=False):
        """Update current project properties.

        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :param bool reset_theme: Reset logo and color
        :param bool reset_logo: Reset logo
        :param bool reset_color: Reset color
        :param bool reset_cname: Reset CNAME
        :param string brand_color: Main color of external panel (e.x: 00ffee)
        :param string logo: Path to logo or URL
        :param string color: Color for project panel
        :param string cname: New CNAME for project
        :param string name: New name for project.
        :rtype: :class:`Project` with new name.
        """
        return self.manager.update(self.id,
                                   name or self.name,
                                   cname=cname,
                                   color=color,
                                   logo=logo,
                                   brand_color=brand_color,
                                   reset_cname=reset_cname,
                                   reset_color=reset_color,
                                   reset_logo=reset_logo,
                                   reset_theme=reset_theme,
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

    def get_quotas(self, region, return_raw=False
                   ) -> Union[Quotas, PartialResponse]:
        """Show quotas info for current project.

        :param string region: name of region
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        """
        return self.manager.quotas_manager.get_project_quotas(
            project_id=self.id, region=region, return_raw=return_raw)

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

    def update_quotas(self, region, quotas, return_raw=False
                      ) -> Union[Quotas, PartialResponse]:
        """Update current project's quotas.

        :param string region: name of region
        :param dict quotas: dict with key `quotas` and keys as dict
                            of items region, zone and value::

                                {
                                    "quotas": {
                                        "compute_cores": [
                                            {
                                                "zone": "ru-1a",
                                                "value": 10
                                            },
                                            {
                                                "zone": "ru-1b",
                                                "value": 10
                                            }
                                        ]
                                    }
                                }
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        """
        return self.manager.quotas_manager.update_project_quotas(
            project_id=self.id, region=region, quotas=quotas,
            return_raw=return_raw)

    def delete(self):
        """Delete current project and all it's objects."""
        return self.manager.delete(self.id)


class ProjectsManager(base.Manager):
    """Manager class for manipulating project."""
    resource_class = Project

    def __init__(self, client, regional_client):
        super(ProjectsManager, self).__init__(client)
        self.roles_manager = RolesManager(client)
        self.quotas_manager = QuotasManager(regional_client)
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

    def create(self, name, skip_quotas_init=False, return_raw=False):
        """Create new project.

        :param string name: Name of project.
        :param skip_quotas_init: flag to skip quotas initialization.
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: list of :class:`Project`.
        """
        body = {
            "project": {
                    "name": name,
                    "skip_quotas_init": skip_quotas_init
                }
        }
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

    @process_theme_params
    def update(self, project_id, name=None, cname=None,
               color=None, logo=None, brand_color=None, reset_cname=False,
               reset_color=False, reset_logo=False, reset_theme=False,
               reset_brand_color=None, return_raw=False):
        """Update Project's properties.

        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :param bool reset_theme: Reset logo and color
        :param bool reset_logo: Reset logo
        :param bool reset_color: Reset color
        :param bool reset_brand_color: Reset brand_color
        :param bool reset_cname: Reset CNAME
        :param string brand_color: Main color of external panel (e.x: 00ffee)
        :param string logo: Path to logo or URL
        :param string color: Color for project panel
        :param string cname: New CNAME for project
        :param string project_id: Project id.
        :param string name: New name for project.
        :rtype: :class:`Project`
        """
        body = {"project": {"theme": {}}}
        if name:
            body["project"]["name"] = name
        if cname:
            body["project"]["custom_url"] = cname
        if color:
            body["project"]["theme"]["color"] = color
        if logo:
            body["project"]["theme"]["logo"] = logo
        if brand_color:
            body["project"]["theme"]["brand_color"] = brand_color
        if reset_cname:
            body["project"]["custom_url"] = ""
        if reset_color:
            body["project"]["theme"]["color"] = ""
        if reset_logo:
            body["project"]["theme"]["logo"] = ""
        if reset_brand_color:
            body["project"]["theme"]["brand_color"] = ""
        if reset_theme:
            body["project"]["theme"].update({"color": "", "logo": "",
                                             "brand_color": ""})
        if not body["project"]["theme"]:
            body["project"].pop("theme")
        return self._patch('/projects/{}'.format(project_id), body, 'project',
                           return_raw=return_raw)

    def delete(self, project_id):
        """Delete Project and all it's objects.

        :param string project_id: Project id."""
        self._delete('/projects/{}'.format(project_id))

    def delete_many(self, project_ids, raise_if_not_found=True):
        """Delete few projects from domain.

        :param list project_ids: Project id's list
        :param bool raise_if_not_found: Raise exception if object won't found
        """

        for project_id in project_ids:
            try:
                self.delete(project_id)
                log.info("Project %s has been deleted", project_id)
            except ClientException as err:
                if raise_if_not_found:
                    raise err
                log.error("%s %s", err, project_id)
