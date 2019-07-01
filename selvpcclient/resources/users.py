import logging

from selvpcclient import base
from selvpcclient.resources.roles import RolesManager
from selvpcclient.exceptions.base import ClientException

log = logging.getLogger(__name__)


class User(base.Resource):
    """Represents a user."""

    def get_roles(self, return_raw=False):
        """List roles for current user.

        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: list of :class:`selvpcclient.resources.roles.Role`
        """
        return self.manager.roles_manager.get_user_roles(self.id,
                                                         return_raw=return_raw)

    def update_name(self, new_name, return_raw=False):
        """Update name for current user.

        :param string new_name: New user name.
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: :class:`User`
        """
        return self.manager.update(self.id, name=new_name,
                                   return_raw=return_raw)

    def update_password(self, new_password, return_raw=False):
        """Update password for current user.

        :param string new_password: New user password.
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: :class:`User`
        """
        return self.manager.update(self.id, password=new_password,
                                   return_raw=return_raw)

    def update_status(self, enabled, return_raw=False):
        """Update status (enabled|disabled) for current user.

        :param bool enabled: New user status: enabled or disabled.
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: :class:`User`
        """
        return self.manager.update(self.id, enabled=enabled,
                                   return_raw=return_raw)

    def add_to_project(self, project_id, return_raw=False):
        """Add current user to project.

        :param str project_id: Project id, where user will be added.
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: :class:`selvpcclient.resources.roles.Role`
        """
        return self.manager.roles_manager.add_user_role_in_project(
            project_id=project_id, user_id=self.id, return_raw=return_raw)

    def remove_from_project(self, project_id):
        """Remove current user from project.

        :param str project_id: Project id, where user will be removed.
        :rtype: None
        """
        self.manager.roles_manager.delete_user_role_from_project(
            project_id=project_id, user_id=self.id)

    def check_in_project(self, project_id):
        """Check if the current user is have a role in project.

        :param str project_id: Project id, where user will be checked.
        :rtype: bool
        """
        roles = self.manager.roles_manager.get_user_roles(self.id)
        for role in roles:
            if role.project_id == project_id:
                return True
        return False

    def delete(self):
        """Delete current user"""
        return self.manager.delete(self.id)


class UsersManager(base.Manager):
    """Manager class for manipulating users."""
    resource_class = User

    def __init__(self, client):
        super(UsersManager, self).__init__(client)
        self.roles_manager = RolesManager(client)

    def list(self, return_raw=False):
        """Get list of all users in current domain.

        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: list of :class:`User`
        """
        return self._list('/users', 'users', return_raw=return_raw)

    def show(self, user_id, return_raw=False):
        """Show detailed info about specific user in current domain.

        :param id: User ID.
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: :class:`User`
        """
        url = '/users/{}'.format(user_id)
        return self._get(url, 'user', return_raw=return_raw)

    def create(self, name, password, enabled, return_raw=False):
        """Create new user in current domain.

        :param string name: User name.
        :param string password: User password.
        :param bool enabled: User status.
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: :class:`User`
        """
        body = {
            "user": {
                "name": name,
                "password": password,
                "enabled": str(enabled).lower() in ['true', '1']
            }
        }
        return self._post('/users', body, 'user', return_raw=return_raw)

    def update(self, user_id,
               name=None,
               password=None,
               enabled=None,
               return_raw=False):
        """Edit user parameters.

        :param string user_id: User id.
        :param string name: New user name. (optional)
        :param string password: New user password. (optional)
        :param bool enabled: New user status. (optional)
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: :class:`User`
        """
        body = {"user": {}}
        if name:
            body["user"]["name"] = name
        if password:
            body["user"]["password"] = password
        if enabled is not None:
            body["user"]["enabled"] = str(enabled).lower() in ['true', '1']
        return self._patch('/users/{}'.format(user_id), body, 'user',
                           return_raw=return_raw)

    def delete(self, user_id):
        """Delete user and it's roles from domain.

        :param string user_id: User id.
        :rtype: None
        """
        self._delete('/users/{}'.format(user_id))

    def delete_many(self, user_ids, raise_if_not_found=True):
        """Delete few users from domain.

        :param list user_ids: User id's list
        :param bool raise_if_not_found: Raise exception if object won't found
        """
        for user_id in user_ids:
            try:
                self.delete(user_id)
                log.info("User %s has been deleted", user_id)
            except ClientException as err:
                if raise_if_not_found:
                    raise err
                log.error("%s %s", err, user_id)
