import responses

from selvpcclient.resources.projects import ProjectsManager
from tests.rest import client
from tests.util import answers, params


@responses.activate
def test_list():
    responses.add(responses.GET, 'http://api/v2/projects',
                  json=answers.PROJECTS_LIST)
    manager = ProjectsManager(client)

    projects = manager.list()

    assert len(projects) > 0


@responses.activate
def test_add():
    responses.add(responses.POST, 'http://api/v2/projects',
                  json=answers.PROJECTS_CREATE)
    manager = ProjectsManager(client)

    project = manager.create(name="Kali")

    assert project is not None


@responses.activate
def test_show():
    responses.add(responses.GET, 'http://api/v2/projects/666',
                  json=answers.PROJECTS_SHOW)
    manager = ProjectsManager(client)

    info = manager.show(project_id='666')

    assert info is not None


@responses.activate
def test_set():
    responses.add(responses.PATCH, 'http://api/v2/projects/666',
                  json=answers.PROJECTS_SET)
    manager = ProjectsManager(client)

    updated_project = manager.update(project_id='666', name="Bonnie")

    assert updated_project is not None


@responses.activate
def test_delete():
    responses.add(responses.DELETE, 'http://api/v2/projects/204', status=204)
    manager = ProjectsManager(client)

    updated_project = manager.delete(project_id=204)

    assert updated_project is None


@responses.activate
def test_get_roles_from_single_obj():
    responses.add(responses.GET, 'http://api/v2/projects',
                  json=answers.PROJECTS_LIST)
    responses.add(responses.GET, 'http://api/v2/roles/projects/'
                                 '15c578ea47a5466db2aeb57dc8443676',
                  json=answers.PROJECTS_SHOW_ROLES)
    manager = ProjectsManager(client)
    projects = manager.list()
    project = projects[0]

    roles = project.get_roles()
    assert len(roles) > 0


@responses.activate
def test_get_quotas_from_single_obj():
    responses.add(responses.GET, 'http://api/v2/projects',
                  json=answers.PROJECTS_LIST)
    responses.add(responses.GET,
                  'http://api/v2/quotas/projects/15c578ea47a5466db2aeb57dc8443676',
                  json=answers.QUOTAS_SHOW)
    project = ProjectsManager(client).list()[0]

    result = project.get_quotas()

    assert result is not None


@responses.activate
def test_update_quotas_from_single_obj():
    responses.add(responses.GET, 'http://api/v2/projects',
                  json=answers.PROJECTS_LIST)
    responses.add(responses.PATCH, 'http://api/v2/quotas/projects/'
                                   '15c578ea47a5466db2aeb57dc8443676',
                  json=answers.QUOTAS_SET)
    manager = ProjectsManager(client)
    projects = manager.list()
    project = projects[0]

    quotas = project.update_quotas({})
    assert quotas is not None


@responses.activate
def test_add_license_from_single_obj():
    responses.add(responses.GET, 'http://api/v2/projects',
                  json=answers.PROJECTS_LIST)
    responses.add(responses.POST, 'http://api/v2/licenses/projects/'
                                  '15c578ea47a5466db2aeb57dc8443676',
                  json=answers.LICENSES_CREATE)
    manager = ProjectsManager(client)
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
    manager = ProjectsManager(client)
    project = manager.list()[0]

    assert project.delete() is None


@responses.activate
def test_set_from_single_obj():
    responses.add(responses.GET, 'http://api/v2/projects',
                  json=answers.PROJECTS_LIST)
    responses.add(responses.PATCH,
                  'http://api/v2/projects/15c578ea47a5466db2aeb57dc8443676',
                  json=answers.PROJECTS_SHOW)
    manager = ProjectsManager(client)
    project = manager.list()[0]

    assert project.update(name="new name project") is not None


@responses.activate
def test_show_from_single_obj():
    responses.add(responses.GET, 'http://api/v2/projects',
                  json=answers.PROJECTS_LIST)
    responses.add(responses.GET,
                  'http://api/v2/quotas/projects/15c578ea47a5466db2aeb57dc8443676',
                  json=answers.QUOTAS_SHOW)
    manager = ProjectsManager(client)
    project = manager.list()[0]

    assert project.get_quotas() is not None


@responses.activate
def test_add_token_from_single_obj():
    responses.add(responses.GET, 'http://api/v2/projects',
                  json=answers.PROJECTS_LIST)
    responses.add(responses.POST, 'http://api/v2/tokens',
                  json=answers.TOKENS_CREATE)
    manager = ProjectsManager(client)
    project = manager.list()[0]

    assert project.add_token() is not None


@responses.activate
def test_add_subnets_from_single_obj():
    responses.add(responses.GET, 'http://api/v2/projects',
                  json=answers.PROJECTS_LIST)
    responses.add(responses.POST, 'http://api/v2/subnets/projects/200',
                  json=answers.SUBNET_ADD)
    manager = ProjectsManager(client)
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
    manager = ProjectsManager(client)
    project = manager.list()[0]
    project.id = 200

    ips = project.add_floating_ips(floatingips=params.floatingips)

    assert len(ips) > 0
