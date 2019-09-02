import responses

from selvpcclient.resources.tokens import TokensManager
from tests.rest import client
from tests.util import answers


@responses.activate
def test_add():
    responses.add(responses.POST, 'http://api/v2/tokens',
                  json=answers.TOKENS_CREATE)

    manager = TokensManager(client)

    token = manager.create(project_id=322)

    assert token is not None


@responses.activate
def test_add_raw():
    responses.add(responses.POST, 'http://api/v2/tokens',
                  json=answers.TOKENS_CREATE)

    manager = TokensManager(client)

    token = manager.create(project_id=322, return_raw=True)

    assert token == answers.TOKENS_CREATE["token"]


@responses.activate
def test_remove():
    responses.add(responses.DELETE, 'http://api/v2/tokens/666', status=204)

    manager = TokensManager(client)

    result = manager.delete(token_id=666)

    assert result is None
