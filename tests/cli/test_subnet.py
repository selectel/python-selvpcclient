import pytest

from tests.cli import make_client, run_cmd
from tests.util import answers

COUNT_OF_SUBNETS = 2


def test_subnet_add():
    client = make_client(return_value=answers.SUBNET_ADD)
    args = ['subnet add',
            'a2e6dd715ca24681b9b335d247b83d16',
            '--region', 'ru-1',
            '--type', 'ipv4',
            '--prefix', '29',
            '--quantity', '2']

    output = run_cmd(args, client, json_output=True)

    assert len(output) == COUNT_OF_SUBNETS
    assert output[0]["id"] == 20


def test_subnet_show():
    client = make_client(return_value=answers.SUBNET_SHOW)
    args = ['subnet show', '6145fba6-dbe2-47af-bad2-6d1dcese5996']

    output = run_cmd(args, client, json_output=True)

    assert output["id"] == 420


def test_subnet_delete_without_accept():
    client = make_client(return_value=None)
    args = ['subnet delete', '6145fba6-dbe2-47af-bad2-6d1dcese5996']

    with pytest.raises(SystemExit):
        run_cmd(args, client)


def test_subnet_list():
    client = make_client(return_value=answers.SUBNET_LIST)
    args = ['subnet list']

    output = run_cmd(args, client, json_output=True)

    assert len(output) == COUNT_OF_SUBNETS
    assert 'servers' not in output[1]
    assert output[0]["id"] == 20
    assert output[1]["id"] == 21


def test_subnet_list_detailed():
    client = make_client(return_value=answers.SUBNET_LIST)
    args = ['subnet list', '--detailed']

    output = run_cmd(args, client, json_output=True)

    assert len(output) == COUNT_OF_SUBNETS
    assert 'servers' in output[1]
    assert output[0]["id"] == 20
    assert output[1]["id"] == 21


def test_subnet_list_with_filters():
    client = make_client(return_value=answers.SUBNET_LIST)

    args = ['subnet list', "--project", "e7081cb46966421fb8b3f3fd9b4db75b"]
    output = run_cmd(args, client, json_output=True)
    assert len(output) == 1
    assert output[0]["project_id"] == 'e7081cb46966421fb8b3f3fd9b4db75b'

    args = ['subnet list', "--region", "ru-1"]
    output = run_cmd(args, client, json_output=True)
    assert len(output) == 1
    assert output[0]["project_id"] == 'e7081cb46966421fb8b3f3fd9b4db75b'

    args = ['subnet list',
            "--project", "e7081cb46966421fb8b3f3fd9b4db75b",
            "--region", "ru-1"]
    output = run_cmd(args, client, json_output=True)
    assert len(output) == 1
    assert output[0]["project_id"] == 'e7081cb46966421fb8b3f3fd9b4db75b'

    args = ['subnet list',
            "--project", "e7081cb46966421fb8b3f3fd9b4db75b",
            "--region", "ru-2"]
    output = run_cmd(args, client, json_output=True)
    assert len(output) == 0


def test_subnets_partial_resp():
    client = make_client(return_value=answers.SUBNETS_PARTIAL)
    args = ['subnet add',
            'e7081cb46966421fb8b3f3fd9b4db75b',
            '--region', 'ru-1',
            '--type', 'ipv4',
            '--quantity', '1']

    output = run_cmd(args, client, json_output=True)
    assert len(output) == 1


def test_subnets_multiple_delete():
    client = make_client(return_value=None)
    args = ["subnet delete",
            "--yes-i-really-want-to-delete",
            "15c578ea47a5466db2aeb57dc8443676",
            "1ec578ea47a5466db2aeb57dc8443672",
            "16c578ea47a5466db2aeb57dc8443676"]
    run_cmd(args, client)
