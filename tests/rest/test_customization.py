import responses

from tests.util import answers
from tests.rest import client

from selvpcclient.resources.customization import CustomizationManager


@responses.activate
def test_customization_raw_return():
    responses.add(
        responses.GET,
        "http://api/v2/theme",
        json=answers.CUSTOMIZATION_SHOW
    )
    manager = CustomizationManager(client)
    result = manager.show(return_raw=True)
    assert result == answers.CUSTOMIZATION_SHOW['theme']
