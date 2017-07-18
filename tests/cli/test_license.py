import pytest

from tests.cli import make_client, run_cmd
from tests.util import answers

COUNT_OF_LICENSES = 2


def test_license_add():
    client = make_client(return_value=answers.LICENSES_CREATE)
    args = [
        'license add',
        'a2e6dd715ca24681b9b335d247b83d16',
        '--type', 'license_windows_2012_standard',
        '-r', 'ru-1',
        '--quantity', '2'
    ]

    output = run_cmd(args, client, json_output=True)

    assert len(output) == COUNT_OF_LICENSES


def test_license_show():
    client = make_client(return_value=answers.LICENSES_SHOW)
    args = ['license show', '420']

    output = run_cmd(args, client, json_output=True)

    assert output["id"] == 420
    assert output["project_id"] == 'e7081cb46966421fb8b3f3fd9b4db75b'


def test_license_delete_without_accept():
    client = make_client(return_value=None)
    args = ['license delete', '15c578ea47a5466db2aeb57dc8443676']

    with pytest.raises(SystemExit):
        run_cmd(args, client)


def test_license_list():
    client = make_client(return_value=answers.LICENSES_LIST)
    args = ['license list']

    output = run_cmd(args, client, json_output=True)

    assert len(output) == COUNT_OF_LICENSES
    for item in output:
        assert 'servers' not in item


def test_license_list_detailed():
    client = make_client(return_value=answers.LICENSES_LIST)
    args = ['license list', '--detailed']

    output = run_cmd(args, client, json_output=True)

    assert len(output) == COUNT_OF_LICENSES
    for item in output:
        assert 'servers' in item


def test_subnet_list_with_filters():
    client = make_client(return_value=answers.LICENSES_LIST)

    args = ['license list', "--project", "e7081cb46966421fb8b3f3fd9b4db75b"]
    output = run_cmd(args, client, json_output=True)
    assert len(output) == 1
    assert output[0]["project_id"] == 'e7081cb46966421fb8b3f3fd9b4db75b'

    args = ['license list', "--region", "ru-1"]
    output = run_cmd(args, client, json_output=True)
    assert len(output) == 1
    assert output[0]["project_id"] == 'e7081cb46966421fb8b3f3fd9b4db75b'

    args = ['license list',
            "--project", "e7081cb46966421fb8b3f3fd9b4db75b",
            "--region", "ru-1"]
    output = run_cmd(args, client, json_output=True)
    assert len(output) == 1
    assert output[0]["project_id"] == 'e7081cb46966421fb8b3f3fd9b4db75b'

    args = ['license list',
            "--project", "e7081cb46966421fb8b3f3fd9b4db75b",
            "--region", "ru-2"]
    output = run_cmd(args, client, json_output=True)
    assert len(output) == 0


def test_licenses_partial_resp():
    client = make_client(return_value=answers.LICENSES_PARTIAL)
    args = ['license add',
            'e7081cb46966421fb8b3f3fd9b4db75b',
            '--region', 'ru-1',
            '--type', 'windows_server_license',
            '--quantity', '1']
    output = run_cmd(args, client, json_output=True)
    assert output == answers.LICENSES_PARTIAL_RESULT


def test_licenses_multiple_delete():
    client = make_client(return_value=None)
    args = ["license delete",
            "--yes-i-really-want-to-delete",
            "15c578ea47a5466db2aeb57dc8443676",
            "1ec578ea47a5466db2aeb57dc8443672",
            "16c578ea47a5466db2aeb57dc8443676"]
    run_cmd(args, client)
