import pytest

from tests.cli import make_client, run_cmd
from tests.util import answers


def test_floatingip_add():
    client = make_client(return_value=answers.FLOATINGIP_ADD)
    args = ['floatingip add',
            'a2e6dd715ca24681b9b335d247b83d16',
            '-r', 'ru-1',
            '--quantity', '1']

    output = run_cmd(args, client, json_output=True)

    assert output[0]["id"] == '0d987b46-bad5-41b7-97e3-bac9974aa97a'
    assert output[0]["project_id"] == 'a2e6dd715ca24681b9b335d247b83d16'


def test_floatingip_show():
    client = make_client(return_value=answers.FLOATINGIP_SHOW)
    args = ['floatingip show', '5b3c296f-b8e2-4ef1-abe7-866b1d3503ca']

    output = run_cmd(args, client, json_output=True)

    assert output[0]["id"] == '0d987b46-bad5-41b7-97e3-bac9974aa97a'
    assert output[0]["project_id"] == 'a2e6dd715ca24681b9b335d247b83d16'


def test_floatingip_delete_without_accept():
    client = make_client(return_value=None)
    args = ['floatingip delete', '15c578ea47a5466db2aeb57dc8443676']

    with pytest.raises(SystemExit):
        run_cmd(args, client)


def test_floatingip_list():
    client = make_client(return_value=answers.FLOATINGIP_LIST)
    args = ['floatingip list']

    output = run_cmd(args, client, json_output=True)

    assert len(output) == 2
    assert output[0]["id"] == '0d987b46-bad5-41b7-97e3-bac9974aa97a'


def test_floatingip_list_with_filters():
    client = make_client(return_value=answers.FLOATINGIP_LIST)

    args = ['floatingip list', "--project", "a2e6dd715ca24681b9b335d247b83d16"]
    output = run_cmd(args, client, json_output=True)
    assert len(output) == 1
    assert output[0]["project_id"] == 'a2e6dd715ca24681b9b335d247b83d16'

    args = ['floatingip list', "--region", "ru-1"]
    output = run_cmd(args, client, json_output=True)
    assert len(output) == 1
    assert output[0]["project_id"] == 'a2e6dd715ca24681b9b335d247b83d16'

    args = ['floatingip list',
            "--project", "a2e6dd715ca24681b9b335d247b83d16",
            "--region", "ru-1"]
    output = run_cmd(args, client, json_output=True)
    assert len(output) == 1
    assert output[0]["project_id"] == 'a2e6dd715ca24681b9b335d247b83d16'

    args = ['floatingip list',
            "--project", "a2e6dd715ca24681b9b335d247b83d16",
            "--region", "ru-2"]
    output = run_cmd(args, client, json_output=True)
    assert len(output) == 0


def test_floating_ips_partial_resp():
    client = make_client(return_value=answers.FLOATING_IPS_PARTIAL)
    args = ["floatingip add",
            "a2e6dd715ca24681b9b335d247b83d16",
            "-r", "ru-1",
            "--quantity", "1"]
    output = run_cmd(args, client, json_output=True)
    assert output == answers.FLOATING_IPS_PARTIAL_RESULT


def test_floating_ips_multiple_delete():
    client = make_client(return_value=None)
    args = ["floatingip delete",
            "--yes-i-really-want-to-delete",
            "15c578ea47a5466db2aeb57dc8443676",
            "1ec578ea47a5466db2aeb57dc8443672",
            "16c578ea47a5466db2aeb57dc8443676"]
    run_cmd(args, client)
