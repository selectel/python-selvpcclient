import pytest

from tests.cli import make_client, run_cmd
from tests.util import answers


def test_user_create():
    client = make_client(return_value=answers.USERS_CREATE)
    args = ['user create',
            '--name', 'user',
            '--password', 'securepassword']

    output = run_cmd(args, client, json_output=True)

    assert output["id"] == 'f9fd1d3167ba4641a3190b4848382216'
    assert output["name"] == 'user'
    assert output["enabled"] is True


def test_user_update():
    client = make_client(return_value=answers.USERS_SET)
    args = ['user update',
            'f9fd1d3167ba4641a3190b4848382216',
            '--name', 'user',
            '--password', 'securepassword']

    output = run_cmd(args, client, json_output=True)

    assert output["id"] == 'f9fd1d3167ba4641a3190b4848382216'
    assert output["name"] == 'user'
    assert output["enabled"] is True


def test_user_delete_without_accept():
    client = make_client(return_value=answers.PROJECTS_SET)
    args = ['user delete', '15c578ea47a5466db2aeb57dc8443676']

    with pytest.raises(SystemExit):
        run_cmd(args, client)


def test_user_list():
    count_of_users = 2
    client = make_client(return_value=answers.USERS_LIST)
    args = ['user list']

    output = run_cmd(args, client, json_output=True)

    assert len(output) == count_of_users
    assert output[0]["id"] == 'f9fd1d3167ba4641a3190b4848382216'
    assert output[1]["id"] == '1d3161d317ba4641a3190b4848382216'


def test_show_nonexistent_user():
    client = make_client(return_value=answers.USERS_EMPTY)
    args = ['user show', 'nonexistent_user']

    with pytest.raises(SystemExit):
        run_cmd(args, client)


def test_show_user():
    client = make_client(return_value=answers.USERS_SHOW)
    args = ['user show', 'f9fd1d3167ba4641a3190b4848382216']

    output = run_cmd(args, client, json_output=True)

    assert output["id"] == 'f9fd1d3167ba4641a3190b4848382216'
    assert output["name"] == 'user'
    assert output["enabled"] is True


def test_user_role_list():
    users_count = 2
    client = make_client(return_value=answers.USERS_ROLE_SHOW)
    args = ['user roles', '1_7354286c9ebf464d86efc16fb56d4fa3']

    output = run_cmd(args, client, json_output=True)

    assert len(output) == users_count
    assert output[0]["project_id"] == '1_7354286c9ebf464d86efc16fb56d4fa3'
    assert output[1]["project_id"] == '1_7354286c9ebf464d86efc16fb56d4fa3'


def test_user_multiple_delete():
    client = make_client(return_value=None)
    args = ["user delete",
            "--yes-i-really-want-to-delete",
            "15c578ea47a5466db2aeb57dc8443676",
            "1ec578ea47a5466db2aeb57dc8443672",
            "16c578ea47a5466db2aeb57dc8443676"]
    run_cmd(args, client)
