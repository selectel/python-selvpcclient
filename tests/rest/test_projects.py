from unittest.mock import patch

import pytest
import responses

from tests.rest import KeystoneTokenInfoMock
from selvpcclient.exceptions.base import ClientException
from selvpcclient.resources.projects import ProjectsManager
from tests.rest import client, regional_client
from tests.util import answers, params


@responses.activate
def test_list():
    responses.add(responses.GET, 'http://api/v2/projects',
                  json=answers.PROJECTS_LIST)
    manager = ProjectsManager(client, regional_client)

    projects = manager.list()

    assert len(projects) > 0


@responses.activate
def test_add():
    responses.add(responses.POST, 'http://api/v2/projects',
                  json=answers.PROJECTS_CREATE)
    manager = ProjectsManager(client, regional_client)

    project = manager.create(name="Kali")

    assert project is not None


@responses.activate
def test_show():
    responses.add(responses.GET, 'http://api/v2/projects/666',
                  json=answers.PROJECTS_SHOW)
    manager = ProjectsManager(client, regional_client)

    info = manager.show(project_id='666')

    assert info is not None


@responses.activate
def test_set():
    responses.add(responses.PATCH, 'http://api/v2/projects/666',
                  json=answers.PROJECTS_SET)
    manager = ProjectsManager(client, regional_client)

    updated_project = manager.update(project_id='666', name="Bonnie")

    assert updated_project is not None


@responses.activate
def test_set_return_raw():
    responses.add(responses.PATCH, 'http://api/v2/projects/666',
                  json=answers.PROJECTS_SET)
    manager = ProjectsManager(client, regional_client)

    updated_project = manager.update(project_id='666', name="Bonnie",
                                     return_raw=True)

    assert updated_project == answers.PROJECTS_SET['project']


@responses.activate
def test_delete():
    responses.add(responses.DELETE, 'http://api/v2/projects/204', status=204)
    manager = ProjectsManager(client, regional_client)

    updated_project = manager.delete(project_id=204)

    assert updated_project is None


@responses.activate
def test_get_roles_from_single_obj():
    responses.add(responses.GET, 'http://api/v2/projects',
                  json=answers.PROJECTS_LIST)
    responses.add(responses.GET, 'http://api/v2/roles/projects/'
                                 '15c578ea47a5466db2aeb57dc8443676',
                  json=answers.PROJECTS_SHOW_ROLES)
    manager = ProjectsManager(client, regional_client)
    projects = manager.list()
    project = projects[0]

    roles = project.get_roles()
    assert len(roles) > 0


@responses.activate
def test_get_quotas_from_single_obj():
    responses.add(responses.GET, 'http://api/v2/projects',
                  json=answers.PROJECTS_LIST)
    responses.add(responses.GET,
                  'http://ru-1.api'
                  '/projects/15c578ea47a5466db2aeb57dc8443676/quotas',
                  json=answers.QUOTAS_SHOW)
    responses.add(responses.GET, 'http://api/v2/accounts',
                  json=answers.ACCOUNT_INFO)
    responses.add(responses.POST, 'http://api/v2/tokens',
                  json=answers.TOKENS_CREATE)

    project = ProjectsManager(client, regional_client).list()[0]

    with patch('keystoneclient.v3.tokens.TokenManager.validate',
               return_value=KeystoneTokenInfoMock()):
        result = project.get_quotas(region='ru-1')

    assert result is not None


@responses.activate
def test_update_quotas_from_single_obj():
    responses.add(responses.GET, 'http://api/v2/projects',
                  json=answers.PROJECTS_LIST)
    responses.add(responses.PATCH,
                  'http://ru-1.api'
                  '/projects/15c578ea47a5466db2aeb57dc8443676/quotas',
                  json=answers.QUOTAS_SET)
    responses.add(responses.GET, 'http://api/v2/accounts',
                  json=answers.ACCOUNT_INFO)
    responses.add(responses.POST, 'http://api/v2/tokens',
                  json=answers.TOKENS_CREATE)
    manager = ProjectsManager(client, regional_client)
    projects = manager.list()
    project = projects[0]

    with patch('keystoneclient.v3.tokens.TokenManager.validate',
               return_value=KeystoneTokenInfoMock()):
        quotas = project.update_quotas(region='ru-1', quotas={})
    assert quotas is not None


@responses.activate
def test_add_license_from_single_obj():
    responses.add(responses.GET, 'http://api/v2/projects',
                  json=answers.PROJECTS_LIST)
    responses.add(responses.POST, 'http://api/v2/licenses/projects/'
                                  '15c578ea47a5466db2aeb57dc8443676',
                  json=answers.LICENSES_CREATE)
    manager = ProjectsManager(client, regional_client)
    projects = manager.list()
    project = projects[0]

    result = project.add_license(licenses=params.licenses)

    assert len(result) > 0


@responses.activate
def test_delete_from_single_obj():
    responses.add(responses.GET, 'http://api/v2/projects',
                  json=answers.PROJECTS_LIST)
    responses.add(responses.DELETE,
                  'http://api/v2/projects/15c578ea47a5466db2aeb57dc8443676',
                  status=204)
    manager = ProjectsManager(client, regional_client)
    project = manager.list()[0]

    assert project.delete() is None


@responses.activate
def test_set_from_single_obj():
    responses.add(responses.GET, 'http://api/v2/projects',
                  json=answers.PROJECTS_LIST)
    responses.add(responses.PATCH,
                  'http://api/v2/projects/15c578ea47a5466db2aeb57dc8443676',
                  json=answers.PROJECTS_SHOW)
    manager = ProjectsManager(client, regional_client)
    project = manager.list()[0]

    assert project.update(name="new name project") is not None


@responses.activate
def test_show_from_single_obj():
    responses.add(responses.GET, 'http://api/v2/projects',
                  json=answers.PROJECTS_LIST)
    responses.add(responses.GET,
                  'http://ru-1.api'
                  '/projects/15c578ea47a5466db2aeb57dc8443676/quotas',
                  json=answers.QUOTAS_SHOW)
    responses.add(responses.GET, 'http://api/v2/accounts',
                  json=answers.ACCOUNT_INFO)
    responses.add(responses.POST, 'http://api/v2/tokens',
                  json=answers.TOKENS_CREATE)
    manager = ProjectsManager(client, regional_client)
    project = manager.list()[0]

    with patch('keystoneclient.v3.tokens.TokenManager.validate',
               return_value=KeystoneTokenInfoMock()):
        quotas = project.get_quotas(region='ru-1')

    assert quotas is not None


@responses.activate
def test_add_token_from_single_obj():
    responses.add(responses.GET, 'http://api/v2/projects',
                  json=answers.PROJECTS_LIST)
    responses.add(responses.POST, 'http://api/v2/tokens',
                  json=answers.TOKENS_CREATE)
    manager = ProjectsManager(client, regional_client)
    project = manager.list()[0]

    assert project.add_token() is not None


@responses.activate
def test_add_subnets_from_single_obj():
    responses.add(responses.GET, 'http://api/v2/projects',
                  json=answers.PROJECTS_LIST)
    responses.add(responses.POST, 'http://api/v2/subnets/projects/200',
                  json=answers.SUBNET_ADD)
    manager = ProjectsManager(client, regional_client)
    project = manager.list()[0]
    project.id = 200

    subnets = project.add_subnet(params.subnets)

    assert len(subnets) > 0


@responses.activate
def test_add_fips_from_single_obj():
    responses.add(responses.GET, 'http://api/v2/projects',
                  json=answers.PROJECTS_LIST)
    responses.add(responses.POST, 'http://api/v2/floatingips/projects/200',
                  json=answers.FLOATINGIP_ADD)
    manager = ProjectsManager(client, regional_client)
    project = manager.list()[0]
    project.id = 200

    ips = project.add_floating_ips(floatingips=params.floatingips)

    assert len(ips) > 0


@responses.activate
def test_get_raw_project_list():
    responses.add(responses.GET, 'http://api/v2/projects',
                  json=answers.PROJECTS_LIST)
    manager = ProjectsManager(client, regional_client)
    project_list_raw = manager.list(return_raw=True)

    assert len(project_list_raw) > 0
    assert project_list_raw == answers.PROJECTS_LIST["projects"]


@responses.activate
def test_delete_multiple_with_raise():
    responses.add(responses.DELETE, 'http://api/v2/projects/100',
                  status=204)
    responses.add(responses.DELETE, 'http://api/v2/projects/200',
                  status=404)

    manager = ProjectsManager(client, regional_client)

    with pytest.raises(ClientException):
        manager.delete_many(project_ids=[100, 200])
