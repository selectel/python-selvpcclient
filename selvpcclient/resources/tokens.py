from selvpcclient import base


class Token(base.Resource):
    """Represents a token."""


class TokensManager(base.Manager):
    """Manager class for manipulating token."""
    resource_class = Token

    def create(self, project_id, return_raw=False):
        """Create reseller token for project.

        :param string project_id: Project_id.
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: :class:`Token`
        """
        body = {'token': {'project_id': project_id}}
        return self._post('/tokens', body, 'token', return_raw=return_raw)
