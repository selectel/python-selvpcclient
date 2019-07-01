import responses

from selvpcclient.resources.capabilities import CapabilitiesManager
from tests.rest import client
from tests.util import answers


@responses.activate
def test_get():
    responses.add(responses.GET, 'http://api/v2/capabilities',
                  json=answers.CAPABILITIES_LIST)

    manager = CapabilitiesManager(client)

    assert manager.get() is not None


@responses.activate
def test_get_raw():
    responses.add(responses.GET, 'http://api/v2/capabilities',
                  json=answers.CAPABILITIES_LIST)

    manager = CapabilitiesManager(client)
    capabilities = manager.get(return_raw=True)

    assert capabilities == answers.CAPABILITIES_LIST["capabilities"]
