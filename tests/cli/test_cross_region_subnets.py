import pytest

from tests.cli import make_client, run_cmd
from tests.util import answers


def test_cross_region_subnet_add():
    client = make_client(return_value=answers.CROSS_REGION_SUBNETS_ADD)
    args = ['subnet cross-region add',
            'a2e6dd715ca24681b9b335d247b83d16',
            '--region', 'ru-1',
            '--region', 'ru-2',
            '--cidr', '192.168.200.0/24',
            '--quantity', '2']

    output = run_cmd(args, client, json_output=True)

    assert output[0]["id"] == 1
    assert output[0]["project_id"] == 'b63ab68796e34858befb8fa2a8b1e12a'


def test_cross_region_subnet_show():
    client = make_client(return_value=answers.CROSS_REGION_SUBNETS_SHOW)
    args = ['subnet cross-region show', '1']

    output = run_cmd(args, client, json_output=True)

    assert output[0]["id"] == 1
    assert output[0]["project_id"] == 'b63ab68796e34858befb8fa2a8b1e12a'


def test_cross_region_subnet_delete_without_accept():
    client = make_client(return_value=None)
    args = ['subnet cross-region delete', '1']

    with pytest.raises(SystemExit):
        run_cmd(args, client)


def test_cross_region_subnet_list():
    client = make_client(return_value=answers.CROSS_REGION_SUBNETS_LIST)
    args = ['subnet cross-region list']

    output = run_cmd(args, client, json_output=True)

    assert len(output) == 2


def test_cross_region_subnet_list_with_filters():
    client = make_client(return_value=answers.CROSS_REGION_SUBNETS_LIST)

    args = ['subnet cross-region list',
            '--project', 'b63ab68796e34858befb8fa2a8b1e12a']
    output = run_cmd(args, client, json_output=True)
    assert len(output) == 1
    assert output[0]["project_id"] == 'b63ab68796e34858befb8fa2a8b1e12a'

    args = ['subnet cross-region list',
            '--project', '857b389e-1b37-40b9-a025-54643b13e589']
    output = run_cmd(args, client, json_output=True)
    assert len(output) == 0


def test_cross_region_subnet_multiple_delete():
    client = make_client(return_value=None)
    args = ['subnet cross-region delete',
            '--yes-i-really-want-to-delete',
            '1', '2']

    run_cmd(args, client)
