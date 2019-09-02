import pytest

from tests.cli import make_client, run_cmd
from tests.util import answers


def test_token_create():
    client = make_client(return_value=answers.TOKENS_CREATE)
    args = ['token create', '--project', 'project_id_here']

    output = run_cmd(args, client, json_output=True)

    assert 'id' in output
    assert 'a9a81014462d499d9d55d3402991f224' in output['id']


def test_domain_token_create():
    client = make_client(return_value=answers.TOKENS_CREATE)
    args = ['token create', '--account', 'account_name']

    output = run_cmd(args, client, json_output=True)

    assert 'id' in output
    assert 'a9a81014462d499d9d55d3402991f224' in output['id']


def test_token_delete_without_accept():
    client = make_client(return_value=None)
    args = ['token delete', 'a9a81014462d499d9d55d3402991f224']

    with pytest.raises(SystemExit):
        run_cmd(args, client)


def test_token_multiple_delete():
    client = make_client(return_value=None)
    args = ["token delete",
            "--yes-i-really-want-to-delete",
            "a9a81014462d499d9d55d3402991f224",
            "a9a81014462d499d9d55d3402991f225",
            "a9a81014462d499d9d55d3402991f226"]
    run_cmd(args, client)
