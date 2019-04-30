from selvpcclient import base


class Token(base.Resource):
    """Represents a token."""


class TokensManager(base.Manager):
    """Manager class for manipulating token."""
    resource_class = Token

    def create(self, project_id=None, account_name=None, return_raw=False):
        """Create reseller token for project.

        :param string project_id: Project_id.
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: :class:`Token`
        """
        body = {'token': {}}
        if project_id:
            body['token']['project_id'] = project_id
        if account_name:
            body['token']['account_name'] = account_name
        return self._post('/tokens', body, 'token', return_raw=return_raw)
