import pytest
import responses

from selvpcclient.exceptions.base import ClientException
from selvpcclient.resources.users import UsersManager
from tests.rest import client
from tests.util import answers


@responses.activate
def test_list():
    responses.add(responses.GET, 'http://api/v2/users',
                  json=answers.USERS_LIST)

    manager = UsersManager(client)

    users = manager.list()

    assert len(users) > 0


@responses.activate
def test_show():
    responses.add(responses.GET, 'http://api/v2/users/666',
                  json=answers.USERS_SHOW)

    manager = UsersManager(client)

    user = manager.show(user_id=666)

    assert user is not None


@responses.activate
def test_add():
    responses.add(responses.POST, 'http://api/v2/users',
                  json=answers.USERS_CREATE)

    manager = UsersManager(client)

    user = manager.create(name="Bonnie", password="Winterbottom",
                          enabled=False)

    assert user is not None


@responses.activate
def test_update():
    responses.add(responses.PATCH, 'http://api/v2/users/666',
                  json=answers.USERS_SET)

    manager = UsersManager(client)

    user = manager.update(
        user_id=666, name="Bonnie", password="Winterbottom", enabled=False
    )

    assert user is not None


@responses.activate
def test_delete():
    responses.add(responses.DELETE, 'http://api/v2/users/666', status=204)

    manager = UsersManager(client)

    result = manager.delete(user_id=666)

    assert result is None


@responses.activate
def test_get_roles_from_single_obj():
    responses.add(responses.GET, 'http://api/v2/users',
                  json=answers.USERS_LIST)
    responses.add(responses.GET, 'http://api/v2/roles/users/12345',
                  json=answers.USERS_ROLE_SHOW)

    user = UsersManager(client).list()[0]
    user.id = 12345

    roles = user.get_roles()

    assert len(roles) > 0


@responses.activate
def test_update_name_from_single_obj():
    responses.add(responses.GET, 'http://api/v2/users',
                  json=answers.USERS_LIST)
    responses.add(responses.PATCH, 'http://api/v2/users/666',
                  json=answers.USERS_SET)

    manager = UsersManager(client)

    user = manager.list()[0]

    user.id = 666
    updated_user = user.update_name("Genry")

    assert updated_user is not None


@responses.activate
def test_update_password_from_single_obj():
    responses.add(responses.GET, 'http://api/v2/users',
                  json=answers.USERS_LIST)
    responses.add(responses.PATCH, 'http://api/v2/users/666',
                  json=answers.USERS_SET)

    manager = UsersManager(client)

    user = manager.list()[0]

    user.id = 666
    updated_user = user.update_password(new_password="secretPassw0rd")

    assert updated_user is not None


@responses.activate
def test_update_status_from_single_obj():
    responses.add(responses.GET, 'http://api/v2/users',
                  json=answers.USERS_LIST)
    responses.add(responses.PATCH, 'http://api/v2/users/666',
                  json=answers.USERS_SET)

    manager = UsersManager(client)

    user = manager.list()[0]

    user.id = 666
    updated_user = user.update_status(enabled=True)

    assert updated_user is not None


@responses.activate
def test_add_user_to_proj_from_single_obj():
    responses.add(responses.GET, 'http://api/v2/users',
                  json=answers.USERS_LIST)
    responses.add(responses.POST, 'http://api/v2/roles/projects/123/users/666',
                  json=answers.ROLES_ADD)

    manager = UsersManager(client)

    user = manager.list()[0]
    user.id = 666

    result = user.add_to_project(project_id=123)

    assert result is not None


@responses.activate
def test_remove_user_to_proj_from_single_obj():
    responses.add(responses.GET, 'http://api/v2/users',
                  json=answers.USERS_LIST)
    responses.add(responses.DELETE,
                  'http://api/v2/roles/projects/100/users/666', status=204)

    manager = UsersManager(client)

    user = manager.list()[0]
    user.id = 666

    assert user.remove_from_project(project_id=100) is None


@responses.activate
def test_check_if_user_in_proj_from_single_obj():
    responses.add(responses.GET, 'http://api/v2/users',
                  json=answers.USERS_LIST)
    responses.add(responses.GET, 'http://api/v2/roles/users/123',
                  json=answers.USERS_ROLE_SHOW)

    manager = UsersManager(client)

    user = manager.list()[0]
    user.id = 123

    assert not user.check_in_project('2_7111116c9ebf464d86efc16fb56d4fa3')
    assert user.check_in_project('1_7354286c9ebf464d86efc16fb56d4fa3')


@responses.activate
def test_list_raw():
    responses.add(responses.GET, 'http://api/v2/users',
                  json=answers.USERS_LIST)

    manager = UsersManager(client)

    users = manager.list(return_raw=True)

    assert users == answers.USERS_LIST["users"]


@responses.activate
def test_delete_multiple_with_raise():
    responses.add(responses.DELETE, 'http://api/v2/users/100',
                  status=204)
    responses.add(responses.DELETE, 'http://api/v2/users/200',
                  status=404)

    manager = UsersManager(client)

    with pytest.raises(ClientException):
        manager.delete_many(user_ids=[100, 200])
