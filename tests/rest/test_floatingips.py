import responses
import pytest

from selvpcclient.exceptions.base import ClientException
from selvpcclient.resources.floatingips import FloatingIPManager
from tests.rest import client
from tests.util import answers, params


@responses.activate
def test_list():
    responses.add(responses.GET, 'http://api/v2/floatingips',
                  json=answers.FLOATINGIP_LIST)
    manager = FloatingIPManager(client)

    ips = manager.list()

    assert len(ips) == 2


@responses.activate
def test_list_with_filters():
    responses.add(responses.GET, 'http://api/v2/floatingips',
                  json=answers.FLOATINGIP_LIST)
    manager = FloatingIPManager(client)

    ips = manager.list(project_id="a2e6dd715ca24681b9b335d247b83d16")
    assert len(ips) == 1
    assert ips[0]["project_id"] == "a2e6dd715ca24681b9b335d247b83d16"

    ips = manager.list(region="ru-2")
    assert len(ips) == 1
    assert ips[0]["region"] == "ru-2"

    ips = manager.list(project_id="a2e6dd715ca24681b9b335d247b83d16",
                       region="ru-2")
    assert len(ips) == 0


@responses.activate
def test_add():
    responses.add(responses.POST, 'http://api/v2/floatingips/projects/200',
                  json=answers.FLOATINGIP_ADD)
    manager = FloatingIPManager(client)

    ips = manager.add(project_id=200, floatingips=params.floatingips)

    assert len(ips) > 0


@responses.activate
def test_show():
    responses.add(responses.GET, 'http://api/v2/floatingips/456',
                  json=answers.FLOATINGIP_SHOW)
    manager = FloatingIPManager(client)

    ip = manager.show(floatingip_id=456)

    assert ip is not None


@responses.activate
def test_delete():
    responses.add(responses.DELETE, 'http://api/v2/floatingips/456',
                  status=204)
    manager = FloatingIPManager(client)

    result = manager.delete(floatingip_id=456)

    assert result is None


@responses.activate
def test_delete_from_single_obj():
    responses.add(responses.GET, 'http://api/v2/floatingips',
                  json=answers.FLOATINGIP_LIST)
    responses.add(responses.DELETE, 'http://api/v2/floatingips/'
                                    '0d987b46-bad5-41b7-97e3-bac9974aa97a',
                  status=204)
    manager = FloatingIPManager(client)
    fip = manager.list()[0]

    result = fip.delete()

    assert result is None


@responses.activate
def test_floatingips_partial_resp():
    responses.add(responses.POST, 'http://api/v2/floatingips/projects/200',
                  json=answers.FLOATING_IPS_PARTIAL,
                  status=207)
    manager = FloatingIPManager(client)

    ips = manager.add(project_id=200,
                      floatingips=params.floatingips)

    assert len(ips) == 2
    assert [ip._info for ip in ips] == answers.FLOATING_IPS_PARTIAL_RESULT


@responses.activate
def test_fips_raw_list():
    responses.add(responses.GET, 'http://api/v2/floatingips',
                  json=answers.FLOATINGIP_LIST)
    manager = FloatingIPManager(client)

    ips = manager.list(return_raw=True)

    assert ips == answers.FLOATINGIP_LIST["floatingips"]


@responses.activate
def test_delete_multiple_with_raise():
    responses.add(responses.DELETE, 'http://api/v2/floatingips/100',
                  status=204)
    responses.add(responses.DELETE, 'http://api/v2/floatingips/200',
                  status=404)

    manager = FloatingIPManager(client)

    with pytest.raises(ClientException):
        manager.delete_many(floatingip_ids=[100, 200])
