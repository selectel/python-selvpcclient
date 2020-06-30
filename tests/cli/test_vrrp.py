import pytest

from tests.cli import make_client, run_cmd
from tests.util import answers


def test_vrrp_add():
    client = make_client(return_value=answers.VRRP_ADD)
    args = ['vrrp add',
            'a2e6dd715ca24681b9b335d247b83d16',
            '--master', 'ru-1',
            '--slave', 'ru-2',
            '--type', 'ipv4',
            '--prefix', '29',
            '--quantity', '3']

    output = run_cmd(args, client, json_output=True)

    assert output[0]["id"] == 6
    assert output[0]["project_id"] == 'b63ab68796e34858befb8fa2a8b1e12a'


def test_vrrp_show():
    client = make_client(return_value=answers.VRRP_SHOW)
    args = ['vrrp show', '2']

    output = run_cmd(args, client, json_output=True)

    assert output[0]["id"] == 2
    assert output[0]["project_id"] == 'b63ab68796e34858befb8fa2a8b1e12a'


def test_vrrp_delete_without_accept():
    client = make_client(return_value=None)
    args = ['vrrp delete', '2']

    with pytest.raises(SystemExit):
        run_cmd(args, client)


def test_vrrp_list():
    client = make_client(return_value=answers.VRRP_LIST)
    args = ['vrrp list']

    output = run_cmd(args, client, json_output=True)

    assert len(output) == 2


def test_vrrp_list_with_filters():
    client = make_client(return_value=answers.VRRP_LIST)

    args = ['vrrp list', "--project", "x63ab68796e34858befb8fa2a8b1e12a"]
    output = run_cmd(args, client, json_output=True)
    assert len(output) == 1
    assert output[0]["project_id"] == 'x63ab68796e34858befb8fa2a8b1e12a'

    args = ['vrrp list',
            "--project", "xxxxx68796e34858befb8fa2a8b1e12a"]
    output = run_cmd(args, client, json_output=True)
    assert len(output) == 0


def test_vrrp_multiple_delete():
    client = make_client(return_value=None)
    args = ["vrrp delete",
            "--yes-i-really-want-to-delete",
            "15c578ea47a5466db2aeb57dc8443676",
            "1ec578ea47a5466db2aeb57dc8443672",
            "16c578ea47a5466db2aeb57dc8443676"]
    run_cmd(args, client)
