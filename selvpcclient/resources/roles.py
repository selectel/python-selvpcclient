from selvpcclient import base


class Role(base.Resource):
    """Represents a role."""

    def delete(self):
        """Delete current user role from project"""
        return self.manager.delete_user_role_from_project(self.project_id,
                                                          self.user_id)


class RolesManager(base.Manager):
    """Manager class for manipulating roles."""
    resource_class = Role

    def get_user_roles(self, user_id, return_raw=False):
        """List roles for the user.

        :param string user_id: User id.
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: list of :class:`Role`
        """
        return self._list('/roles/users/{}'.format(user_id), 'roles',
                          return_raw=return_raw)

    def get_domain_roles(self, return_raw=False):
        """List all roles for all projects in the domain.

        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: list of :class:`Role`
        """
        return self._list('/roles', 'roles', return_raw=return_raw)

    def get_project_roles(self, project_id, return_raw=False):
        """List all roles for the project.

        :param string project_id: Project id.
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: list of :class:`Role`
        """
        return self._list('/roles/projects/{}'.format(project_id), 'roles',
                          return_raw=return_raw)

    def add(self, roles, return_raw=False):
        """Bulk create user <-> project roles for given input.

        :param dict roles: Dict with key `roles` and keys as dict
                           of items project_id and user_id::

                               {
                                   "roles": [{
                                       "project_id": "7354286c9ebf464d86efc1",
                                       "user_id": "5900efc62db34decae9f2dbc0"
                                   }]
                               }
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: list of :class:`Role`
        """
        return self._list('/roles', body=roles, response_key='roles',
                          return_raw=return_raw)

    def add_user_role_in_project(self, project_id, user_id, return_raw=False):
        """Create user <-> project role.

        :param string project_id: Project id.
        :param string user_id: User id.
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: :class:`Role`
        """
        url = '/roles/projects/{}/users/{}'.format(project_id, user_id)
        return self._post(url=url, body=None, response_key='role',
                          return_raw=return_raw)

    def delete_user_role_from_project(self, project_id, user_id):
        """Delete user <-> project role.

        :param string project_id: Project id.
        :param string user_id: User id.
        """
        url = '/roles/projects/{}/users/{}'.format(project_id, user_id)
        self._delete(url)
