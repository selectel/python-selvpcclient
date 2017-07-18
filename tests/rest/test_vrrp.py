import pytest
import responses

from selvpcclient.exceptions.base import ClientException
from selvpcclient.resources.vrrp import VRRPManager
from tests.rest import client
from tests.util import answers, params


@responses.activate
def test_list():
    responses.add(responses.GET, 'http://api/v2/vrrp_subnets',
                  json=answers.VRRP_LIST)

    manager = VRRPManager(client)

    subnets = manager.list()
    assert len(subnets) == 2


@responses.activate
def test_list_with_filters():
    responses.add(responses.GET, 'http://api/v2/vrrp_subnets',
                  json=answers.VRRP_LIST)

    manager = VRRPManager(client)

    ips = manager.list(project_id="x63ab68796e34858befb8fa2a8b1e12a")
    assert len(ips) == 1
    assert ips[0]["project_id"] == "x63ab68796e34858befb8fa2a8b1e12a"

    ips = manager.list(project_id="e7081cb46966421fb8b3f3fd9b4db75b")
    assert len(ips) == 0


@responses.activate
def test_add():
    responses.add(responses.POST, 'http://api/v2/vrrp_subnets/projects/200',
                  json=answers.VRRP_ADD)

    manager = VRRPManager(client)

    subnets = manager.add(project_id=200, vrrp=params.vrrp)

    assert len(subnets) > 0


@responses.activate
def test_show():
    responses.add(responses.GET, 'http://api/v2/vrrp_subnets/666',
                  json=answers.VRRP_SHOW)

    manager = VRRPManager(client)

    vrrp = manager.show(vrrp_id=666)

    assert vrrp is not None


@responses.activate
def test_delete():
    responses.add(responses.DELETE, 'http://api/v2/vrrp_subnets/456',
                  status=204)

    manager = VRRPManager(client)

    result = manager.delete(vrrp_id=456)

    assert result is None


@responses.activate
def test_delete_from_single_obj():
    responses.add(responses.GET, 'http://api/v2/vrrp_subnets',
                  json=answers.VRRP_LIST)
    responses.add(responses.DELETE, 'http://api/v2/vrrp_subnets/3',
                  status=204)

    manager = VRRPManager(client)

    vrrp = manager.list()[0]
    result = vrrp.delete()

    assert result is None


@responses.activate
def test_list_raw():
    responses.add(responses.GET, 'http://api/v2/vrrp_subnets',
                  json=answers.VRRP_LIST)

    manager = VRRPManager(client)

    subnets = manager.list(return_raw=True)
    assert subnets == answers.VRRP_LIST["vrrp_subnets"]


@responses.activate
def test_delete_multiple_with_raise():
    responses.add(responses.DELETE, 'http://api/v2/vrrp_subnets/100',
                  status=204)
    responses.add(responses.DELETE, 'http://api/v2/vrrp_subnets/200',
                  status=404)

    manager = VRRPManager(client)

    with pytest.raises(ClientException):
        manager.delete_many(vrrp_ids=[100, 200])
