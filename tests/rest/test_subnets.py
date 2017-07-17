import pytest
import responses

from selvpcclient.exceptions.base import ClientException
from selvpcclient.resources.subnets import SubnetManager
from tests.rest import client
from tests.util import answers, params


@responses.activate
def test_list():
    responses.add(responses.GET, 'http://api/v2/subnets',
                  json=answers.SUBNET_LIST)

    manager = SubnetManager(client)

    subnets = manager.list()
    assert len(subnets) == 2


@responses.activate
def test_list_with_filters():
    responses.add(responses.GET, 'http://api/v2/subnets',
                  json=answers.SUBNET_LIST)

    manager = SubnetManager(client)

    ips = manager.list(project_id="e7081cb46966421fb8b3f3fd9b4db75b")
    assert len(ips) == 1
    assert ips[0]["project_id"] == "e7081cb46966421fb8b3f3fd9b4db75b"

    ips = manager.list(region="ru-2")
    assert len(ips) == 1
    assert ips[0]["region"] == "ru-2"

    ips = manager.list(project_id="e7081cb46966421fb8b3f3fd9b4db75b",
                       region="ru-2")
    assert len(ips) == 0


@responses.activate
def test_add():
    responses.add(responses.POST, 'http://api/v2/subnets/projects/200',
                  json=answers.SUBNET_ADD)

    manager = SubnetManager(client)

    subnets = manager.add(project_id=200, subnets=params.subnets)

    assert len(subnets) > 0


@responses.activate
def test_show():
    responses.add(responses.GET, 'http://api/v2/subnets/666',
                  json=answers.SUBNET_SHOW)

    manager = SubnetManager(client)

    subnet = manager.show(subnet_id=666)

    assert subnet is not None


@responses.activate
def test_delete():
    responses.add(responses.DELETE, 'http://api/v2/subnets/456', status=204)

    manager = SubnetManager(client)

    result = manager.delete(subnet_id=456)

    assert result is None


@responses.activate
def test_delete_from_single_obj():
    responses.add(responses.GET, 'http://api/v2/subnets',
                  json=answers.SUBNET_LIST)
    responses.add(responses.DELETE, 'http://api/v2/subnets/20', status=204)

    manager = SubnetManager(client)

    subnet = manager.list()[0]
    result = subnet.delete()

    assert result is None


@responses.activate
def test_subnets_partial_resp():
    responses.add(responses.POST, 'http://api/v2/subnets/projects/200',
                  json=answers.SUBNETS_PARTIAL,
                  status=207)

    manager = SubnetManager(client)

    subnets = manager.add(project_id=200, subnets=params.subnets)

    assert len(subnets) == 1
    assert [sub._info for sub in subnets] == answers.SUBNETS_PARTIAL_RESULT


@responses.activate
def test_list_raw():
    responses.add(responses.GET, 'http://api/v2/subnets',
                  json=answers.SUBNET_LIST)

    manager = SubnetManager(client)

    subnets = manager.list(return_raw=True)
    assert subnets == answers.SUBNET_LIST["subnets"]


@responses.activate
def test_delete_multiple_with_raise():
    responses.add(responses.DELETE, 'http://api/v2/subnets/100',
                  status=204)
    responses.add(responses.DELETE, 'http://api/v2/subnets/200',
                  status=404)

    manager = SubnetManager(client)

    with pytest.raises(ClientException):
        manager.delete_many(subnet_ids=[100, 200])
