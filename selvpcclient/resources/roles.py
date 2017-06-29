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

    def get_user_roles(self, user_id):
        """List roles for the user.

        :param string user_id: User id.
        :rtype: list of :class:`Role`
        """
        return self._list('/roles/users/{}'.format(user_id), 'roles')

    def get_project_roles(self, project_id):
        """List all roles for the project.

        :param string project_id: Project id.
        :rtype: list of :class:`Role`
        """
        return self._list('/roles/projects/{}'.format(project_id), 'roles')

    def add(self, roles):
        """Bulk create user <-> project roles for given input.

        :param dict roles: Dict with key `roles` and keys as dict
                           of items project_id and user_id::

                               {
                                   "roles": [{
                                       "project_id": "7354286c9ebf464d86efc1",
                                       "user_id": "5900efc62db34decae9f2dbc0"
                                   }]
                               }
        :rtype: list of :class:`Role`
        """
        return self._list('/roles', body=roles, response_key='roles')

    def add_user_role_in_project(self, project_id, user_id):
        """Create user <-> project role.

        :param string project_id: Project id.
        :param string user_id: User id.
        :rtype: :class:`Role`
        """
        url = '/roles/projects/{}/users/{}'.format(project_id, user_id)
        return self._post(url=url, body='', response_key='role')

    def delete_user_role_from_project(self, project_id, user_id):
        """Delete user <-> project role.

        :param string project_id: Project id.
        :param string user_id: User id.
        """
        url = '/roles/projects/{}/users/{}'.format(project_id, user_id)
        self._delete(url)
