import pytest

from tests.cli import make_client, run_cmd
from tests.util import answers


def test_project_create():
    client = make_client(return_value=answers.PROJECTS_CREATE)
    args = ['project create', '--name', 'project1']

    output = run_cmd(args, client, json_output=True)

    assert output["name"] == 'project1'
    assert output["id"] == '15c578ea47a5466db2aeb57dc8443676'
    assert output["enabled"] is True
    assert "url" in output


def test_project_update():
    client = make_client(return_value=answers.PROJECTS_SET)
    args = ['project update',
            '15c578ea47a5466db2aeb57dc8443676',
            '--name', 'project1']

    output = run_cmd(args, client, json_output=True)

    assert output["name"] == 'project1'
    assert output["id"] == '15c578ea47a5466db2aeb57dc8443676'
    assert output["enabled"] is True
    assert "url" in output


def test_project_show():
    client = make_client(return_value=answers.PROJECTS_SET)
    args = ['project show', '15c578ea47a5466db2aeb57dc8443676']

    output = run_cmd(args, client, json_output=True)

    assert output["name"] == 'project1'
    assert output["id"] == '15c578ea47a5466db2aeb57dc8443676'
    assert output["enabled"] is True
    assert "url" in output


def test_project_delete_without_accept():
    client = make_client(return_value=answers.PROJECTS_SET)
    args = ['project delete', '15c578ea47a5466db2aeb57dc8443676']

    with pytest.raises(SystemExit):
        run_cmd(args, client)


def test_project_list():
    projects_count = 2
    client = make_client(return_value=answers.PROJECTS_LIST)
    args = ['project list']

    output = run_cmd(args, client, json_output=True)

    assert len(output) == projects_count
    assert output[0]["id"] == '15c578ea47a5466db2aeb57dc8443676'
    assert output[1]["id"] == '2c578ea47a5466db2aeb57dc8443676'
