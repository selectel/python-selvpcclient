import pytest
import responses

from selvpcclient.exceptions.base import ClientException
from selvpcclient.resources.keypairs import KeyPairManager
from tests.rest import client
from tests.util import answers, params


@responses.activate
def test_list():
    responses.add(responses.GET, 'http://api/v2/keypairs',
                  json=answers.KEYPAIR_LIST)

    manager = KeyPairManager(client)

    pairs = manager.list()
    assert len(pairs) == 2


@responses.activate
def test_add():
    responses.add(responses.POST, 'http://api/v2/keypairs',
                  json=answers.KEYPAIR_ADD)

    manager = KeyPairManager(client)

    keypair = manager.add(keypair=params.keypair)

    assert len(keypair) > 0


@responses.activate
def test_delete():
    responses.add(responses.DELETE,
                  'http://api/v2/keypairs/MOSCOW_KEY'
                  '/users/88ad5569d8c64f828ac3d2efa4e552dd',
                  status=204)

    manager = KeyPairManager(client)

    result = manager.delete(user_id='88ad5569d8c64f828ac3d2efa4e552dd',
                            key_name='MOSCOW_KEY')

    assert result is None


@responses.activate
def test_delete_from_single_obj():
    responses.add(responses.GET,
                  'http://api/v2/keypairs',
                  json=answers.KEYPAIR_LIST)
    responses.add(responses.DELETE,
                  'http://api/v2/keypairs/User_1'
                  '/users/88ad5569d8c64f828ac3d2efa4e552dd',
                  status=204)

    manager = KeyPairManager(client)

    keypair = manager.list()[0]
    result = keypair.delete()

    assert result is None


@responses.activate
def test_list_raw():
    responses.add(responses.GET, 'http://api/v2/keypairs',
                  json=answers.KEYPAIR_LIST)

    manager = KeyPairManager(client)

    keypairs = manager.list(return_raw=True)
    assert keypairs == answers.KEYPAIR_LIST["keypairs"]


@responses.activate
def test_delete_multiple_with_raise():
    responses.add(responses.DELETE,
                  'http://api/v2/keypairs/User_1'
                  '/users/88ad5569d8c64f828ac3d2efa4e552dd',
                  status=204)
    responses.add(responses.DELETE,
                  'http://api/v2/keypairs/User_2'
                  '/users/88ad5569d8c64f828ac3d2efa4e552dd',
                  status=404)

    manager = KeyPairManager(client)

    with pytest.raises(ClientException):
        manager.delete_many(user_id='88ad5569d8c64f828ac3d2efa4e552dd',
                            key_names=["User_1", "User_2"])
