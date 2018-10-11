import pytest
import responses

from selvpcclient.exceptions.base import ClientException
from selvpcclient.resources.cross_region_subnets import \
    CrossRegionSubnetManager
from tests.rest import client
from tests.util import answers, params


@responses.activate
def test_list():
    responses.add(responses.GET, 'http://api/v2/cross_region_subnets',
                  json=answers.CROSS_REGION_SUBNETS_LIST)

    manager = CrossRegionSubnetManager(client)

    subnets = manager.list()
    assert len(subnets) == 2


@responses.activate
def test_list_with_filters():
    responses.add(responses.GET, 'http://api/v2/cross_region_subnets',
                  json=answers.CROSS_REGION_SUBNETS_LIST)

    manager = CrossRegionSubnetManager(client)

    subnets = manager.list(project_id="b63ab68796e34858befb8fa2a8b1e12a")
    assert len(subnets) == 1
    assert subnets[0]["project_id"] == "b63ab68796e34858befb8fa2a8b1e12a"

    subnets = manager.list(project_id="1af85e2e-9a9f-44d0-9361-ef68cd126a76")
    assert len(subnets) == 0


@responses.activate
def test_add():
    responses.add(
        responses.POST,
        'http://api/v2/cross_region_subnets/projects/'
        '2f936ccf-f2c0-4041-8c80-5f369cd20412',
        json=answers.CROSS_REGION_SUBNETS_ADD)

    manager = CrossRegionSubnetManager(client)

    subnets = manager.add(
        project_id='2f936ccf-f2c0-4041-8c80-5f369cd20412',
        cross_region_subnets=params.cross_region_subnets)

    assert len(subnets) > 0


@responses.activate
def test_show():
    responses.add(responses.GET, 'http://api/v2/cross_region_subnets/1',
                  json=answers.CROSS_REGION_SUBNETS_SHOW)

    manager = CrossRegionSubnetManager(client)

    cross_region_subnet = manager.show(cross_region_subnet_id=1)

    assert cross_region_subnet is not None


@responses.activate
def test_delete():
    responses.add(responses.DELETE, 'http://api/v2/cross_region_subnets/1',
                  status=204)

    manager = CrossRegionSubnetManager(client)

    result = manager.delete(cross_region_subnet_id=1)

    assert result is None


@responses.activate
def test_delete_from_single_obj():
    responses.add(responses.GET, 'http://api/v2/cross_region_subnets',
                  json=answers.CROSS_REGION_SUBNETS_LIST)
    responses.add(responses.DELETE, 'http://api/v2/cross_region_subnets/1',
                  status=204)

    manager = CrossRegionSubnetManager(client)

    cross_region_subnet = manager.list()[0]
    result = cross_region_subnet.delete()

    assert result is None


@responses.activate
def test_list_raw():
    responses.add(responses.GET, 'http://api/v2/cross_region_subnets',
                  json=answers.CROSS_REGION_SUBNETS_LIST)

    manager = CrossRegionSubnetManager(client)

    subnets = manager.list(return_raw=True)
    assert subnets == answers.CROSS_REGION_SUBNETS_LIST["cross_region_subnets"]


@responses.activate
def test_delete_multiple_with_raise():
    responses.add(responses.DELETE, 'http://api/v2/cross_region_subnets/1',
                  status=204)
    responses.add(responses.DELETE, 'http://api/v2/cross_region_subnets/2',
                  status=404)

    manager = CrossRegionSubnetManager(client)

    with pytest.raises(ClientException):
        manager.delete_many(cross_region_subnet_ids=[1, 2])
