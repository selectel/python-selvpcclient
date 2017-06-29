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
