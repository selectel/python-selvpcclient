import logging

from selvpcclient import base
from selvpcclient.exceptions.base import ClientException

log = logging.getLogger(__name__)


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

    def delete(self, token_id):
        """Delete reseller owned token.

        :param string token_id: Token id.
        :rtype: None
        """
        self._delete('/tokens/{}'.format(token_id))

    def delete_many(self, token_ids, raise_if_not_found=True):
        """Delete few reseller tokens.

        :param list token_ids: Token id's list
        :param bool raise_if_not_found: Raise exception if object won't found
        """
        for token_id in token_ids:
            try:
                self.delete(token_id)
                log.info("Token %s has been deleted", token_id)
            except ClientException as err:
                if raise_if_not_found:
                    raise err
                log.error("%s %s", err, token_id)
