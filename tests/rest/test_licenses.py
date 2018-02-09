import pytest
import responses

from selvpcclient.exceptions.base import ClientException
from selvpcclient.resources.licenses import LicenseManager
from tests.rest import client
from tests.util import answers, params


@responses.activate
def test_list():
    responses.add(responses.GET, 'http://api/v2/licenses',
                  json=answers.LICENSES_LIST)
    manager = LicenseManager(client)

    licenses = manager.list()

    assert len(licenses) == 2


@responses.activate
def test_list_with_filters():
    responses.add(responses.GET, 'http://api/v2/licenses',
                  json=answers.LICENSES_LIST)
    manager = LicenseManager(client)

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
    responses.add(responses.POST, 'http://api/v2/licenses/projects/666',
                  json=answers.LICENSES_CREATE)
    manager = LicenseManager(client)

    licenses = manager.add(project_id=666, licenses=params.licenses)

    assert len(licenses) > 0


@responses.activate
def test_delete():
    responses.add(responses.DELETE, 'http://api/v2/licenses/777', status=204)
    manager = LicenseManager(client)

    result = manager.delete(license_id=777)

    assert result is None


@responses.activate
def test_show():
    responses.add(responses.GET, 'http://api/v2/licenses/awesome_id',
                  json=answers.LICENSES_SHOW)
    manager = LicenseManager(client)

    license = manager.show(license_id="awesome_id")

    assert license is not None
    assert license.id == 420


@responses.activate
def test_delete_from_single_obj():
    responses.add(responses.GET, 'http://api/v2/licenses',
                  json=answers.LICENSES_LIST)
    responses.add(responses.DELETE, 'http://api/v2/licenses/0', status=204)
    manager = LicenseManager(client)

    license = manager.list()[0]
    result = license.delete()

    assert result is None


@responses.activate
def test_licenses_partial_resp():
    responses.add(responses.POST, 'http://api/v2/licenses/projects/666',
                  json=answers.LICENSES_PARTIAL,
                  status=207)
    manager = LicenseManager(client)

    licenses = manager.add(project_id=666, licenses=params.licenses)

    assert len(licenses) == 1
    assert [lic._info for lic in licenses] == answers.LICENSES_PARTIAL_RESULT


@responses.activate
def test_raw_list():
    responses.add(responses.GET, 'http://api/v2/licenses',
                  json=answers.LICENSES_LIST)
    manager = LicenseManager(client)

    licenses = manager.list(return_raw=True)

    assert licenses == answers.LICENSES_LIST["licenses"]


@responses.activate
def test_delete_multiple_with_raise():
    responses.add(responses.DELETE, 'http://api/v2/licenses/100',
                  status=204)
    responses.add(responses.DELETE, 'http://api/v2/licenses/200',
                  status=404)

    manager = LicenseManager(client)

    with pytest.raises(ClientException):
        manager.delete_many(license_ids=[100, 200])
