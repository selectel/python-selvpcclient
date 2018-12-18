import responses

from selvpcclient.resources.roles import RolesManager
from tests.rest import client
from tests.util import answers
from tests.util import params


@responses.activate
def test_add_roles_by_dict():
    responses.add(responses.POST, 'http://api/v2/roles',
                  json=answers.ROLES_LIST)

    manager = RolesManager(client)

    result = manager.add(roles=params.roles)

    assert len(result) > 0


@responses.activate
def test_add_role_by_single_obj():
    responses.add(responses.POST, 'http://api/v2/roles',
                  json=answers.ROLES_LIST)

    manager = RolesManager(client)

    result = manager.add(roles=params.roles)

    assert len(result) > 0


@responses.activate
def test_get_project_roles():
    responses.add(responses.GET, 'http://api/v2/roles/projects/123',
                  json=answers.PROJECTS_SHOW_ROLES)

    manager = RolesManager(client)

    result = manager.get_project_roles(project_id=123)

    assert len(result) > 0


@responses.activate
def test_get_domain_roles():
    responses.add(responses.GET, 'http://api/v2/roles',
                  json=answers.PROJECTS_SHOW_ROLES)

    manager = RolesManager(client)

    result = manager.get_domain_roles()

    assert len(result) > 0


@responses.activate
def test_create_user_role_in_project():
    responses.add(responses.POST, 'http://api/v2/roles/projects/123/users/666',
                  json=answers.ROLES_ADD)

    manager = RolesManager(client)

    result = manager.add_user_role_in_project(project_id=123, user_id=666)

    assert result is not None


@responses.activate
def test_get_user_roles():
    responses.add(responses.GET, 'http://api/v2/roles/users/666',
                  json=answers.USERS_ROLE_SHOW)

    manager = RolesManager(client)

    result = manager.get_user_roles(user_id=666)

    assert len(result) > 0


@responses.activate
def test_delete_user_role_from_project():
    responses.add(responses.DELETE,
                  'http://api/v2/roles/projects/100/users/666', status=204)

    manager = RolesManager(client)

    result = manager.delete_user_role_from_project(project_id=100, user_id=666)

    assert result is None


@responses.activate
def test_roles_partial_resp():
    responses.add(responses.POST, 'http://api/v2/roles',
                  json=answers.ROLES_PARTIAL,
                  status=207)

    manager = RolesManager(client)

    result = manager.add(roles=params.roles)

    assert len(result) == 1
    assert [role._info for role in result] == answers.ROLES_PARTIAL_RESULT


@responses.activate
def test_get_user_raw_roles():
    responses.add(responses.GET, 'http://api/v2/roles/users/666',
                  json=answers.USERS_ROLE_SHOW)

    manager = RolesManager(client)

    result = manager.get_user_roles(user_id=666, return_raw=True)

    assert result == answers.USERS_ROLE_SHOW["roles"]
