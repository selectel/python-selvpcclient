import pytest

from tests.cli import make_client, run_cmd
from tests.util import answers


def test_role_add():
    client = make_client(return_value=answers.ROLES_ADD)
    args = ['role create',
            '-p 1_7354286c9ebf464d86efc16fb56d4fa3',
            '-u 5900efc62db34decae9f2dbc04a8ce0f']

    output = run_cmd(args, client, json_output=True)

    assert output["project_id"] == '1_7354286c9ebf464d86efc16fb56d4fa3'
    assert output["user_id"] == '5900efc62db34decae9f2dbc04a8ce0f'


def test_role_delete_without_accept():
    client = make_client(return_value=None)
    args = ['role delete',
            '-p 1_7354286c9ebf464d86efc16fb56d4fa3',
            '-u 5900efc62db34decae9f2dbc04a8ce0f']

    with pytest.raises(SystemExit):
        run_cmd(args, client)


def test_role_list_for_domain():
    count_of_roles = 2
    client = make_client(return_value=answers.ROLES_LIST)
    args = ['role list', '--all']

    output = run_cmd(args, client, json_output=True)

    assert len(output) == count_of_roles
    assert output[0]["project_id"] == '1_7354286c9ebf464d86efc16fb56d4fa3'
    assert output[1]["project_id"] == '1_7354286c9ebf464d86efc16fb56d4fa3'
    assert output[0]["user_id"] == '1900efc62db34decae9f2dbc04a8ce0f'
    assert output[1]["user_id"] == '5900efc62db34decae9f2dbc04a8ce0f'


def test_role_list_filter_by_project():
    count_of_roles = 2
    client = make_client(return_value=answers.ROLES_LIST)
    args = ['role list', '--project', '1_7354286c9ebf464d86efc16fb56d4fa3']

    output = run_cmd(args, client, json_output=True)

    assert len(output) == count_of_roles
    assert output[0]["project_id"] == '1_7354286c9ebf464d86efc16fb56d4fa3'
    assert output[1]["project_id"] == '1_7354286c9ebf464d86efc16fb56d4fa3'
    assert output[0]["user_id"] == '1900efc62db34decae9f2dbc04a8ce0f'
    assert output[1]["user_id"] == '5900efc62db34decae9f2dbc04a8ce0f'
