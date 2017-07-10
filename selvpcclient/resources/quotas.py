from selvpcclient import base


class Quotas(base.Resource):
    """Represents a quota."""


class QuotasManager(base.Manager):
    """Manager class for manipulating quota."""
    resource_class = Quotas

    def get_domain_quotas(self, return_raw=False):
        """Get total amount of resources available to be allocated to projects.

        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: :class:`Quotas`
        """
        return self._get('/quotas', 'quotas', return_raw=return_raw)

    def get_free_domain_quotas(self, return_raw=False):
        """Get amount of resources available to be allocated to projects.

        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: :class:`Quotas`
        """
        return self._get('/quotas/free', 'quotas', return_raw=return_raw)

    def get_projects_quotas(self, return_raw=False):
        """Show quotas info for all domain projects.

        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: :class:`Quotas`
        """
        return self._get('/quotas/projects', 'quotas', return_raw=return_raw)

    def get_project_quotas(self, project_id, return_raw=False):
        """Show quotas info for one project.

        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :param string project_id: Project id.
        :rtype: :class:`Quotas`
        """
        return self._get('/quotas/projects/{}'.format(project_id), 'quotas',
                         return_raw=return_raw)

    def update(self, project_id, quotas, return_raw=False):
        """Update Project's quotas.

        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :param string project_id: Project id.
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
        :rtype: :class:`Quotas`
        """

        url = '/quotas/projects/{}'.format(project_id)
        return self._patch(url=url, body=quotas, response_key='quotas',
                           return_raw=return_raw)

    def optimize_project_quotas(self, project_id, return_raw=False):
        """Optimize project quotas.

        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :param string project_id: Project id.
        """

        body = {"quotas": {}}
        quotas = self.get_project_quotas(project_id)._info
        for resource, quotas_ in quotas.items():
            for quota in quotas_:
                if quota["value"] == 0 or quota["value"] == quota["used"]:
                    continue

                if resource not in body["quotas"]:
                    body["quotas"][resource] = []

                quota["value"] = quota["used"]
                del quota["used"]
                body["quotas"][resource].append(quota)

        if not body["quotas"]:
            return None

        return self.update(project_id, quotas=body, return_raw=return_raw)
