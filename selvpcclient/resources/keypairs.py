import logging

from selvpcclient import base
from selvpcclient.exceptions.base import ClientException
from selvpcclient.util import process_pair_params

log = logging.getLogger(__name__)


class KeyPair(base.Resource):
    """Represents a keypair."""

    def delete(self):
        """Delete current keypair from domain."""
        self.manager.delete(self.user_id, self.name)


class KeyPairManager(base.Manager):
    """Manager class for manipulating keypairs."""
    resource_class = KeyPair

    def list(self, return_raw=False, user_id=None):
        """Get list of all keypairs for domain.

        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :param string user_id: optional filter of keypairs by User id.
        :rtype: list of :class:`Keypair`
        """
        url = '/keypairs'
        if user_id:
            url = url + '?user_id={}'.format(user_id)
        return self._list(url, 'keypairs', return_raw=return_raw)

    @process_pair_params
    def add(self, keypair, return_raw=False):
        """Add keypair to domain. (include all regions)

        :param dict keypair: Dict with key `keypair`:

                                {
                                    "keypair": {
                                        "user_id": "b832ef...94469d",
                                        "name": "my_key_name",
                                        "public_key": "ssh ... name@name",
                                        "regions": ["ru-1", "ru-2"]
                                    }
                                }
        :param return_raw: flag to force returning raw JSON instead of
                Python object of self.resource_class
        :rtype: list of :class:`Keypair`
        """
        return self._list('/keypairs', 'keypair', body=keypair,
                          return_raw=return_raw)

    def delete(self, user_id, key_name):
        """Delete keypair from all regions."""
        self._delete('/keypairs/{}/users/{}'.format(key_name, user_id))

    def delete_many(self, user_id, key_names, raise_if_not_found=True):
        """Delete few subnets from domain.

        :param str user_id: User that store a keypair
        :param list key_names: Keypair names
        :param bool raise_if_not_found: Raise exception if object won't found
        """

        for name in key_names:
            try:
                self.delete(user_id, name)
                log.info("Keypair %s has been deleted for %s", name, user_id)
            except ClientException as err:
                if raise_if_not_found:
                    raise err
                log.error("%s %s %s", err, user_id, name)
