import pytest

from tests.cli import make_client, run_cmd
from tests.util import answers


def test_keypair_list():
    client = make_client(return_value=answers.KEYPAIR_LIST)

    args = ["keypair list"]

    output = run_cmd(args, client, json_output=True)

    assert len(output) == 2


def test_keypair_list_filter():
    client = make_client(return_value=answers.KEYPAIR_LIST)

    args = ["keypair list",
            "--user", "88ad5569d8c64f828ac3d2efa4e552dd"]

    output = run_cmd(args, client, json_output=True)

    assert len(output) == 2


def test_keypair_add():
    client = make_client(return_value=answers.KEYPAIR_ADD)

    args = ["keypair add",
            "--user", "88ad5569d8c64f828ac3d2efa4e552dd",
            "--name", "MOSCOW_KEY",
            "--key", "ssh-rsa ssh-rsa ... user@name"]

    output = run_cmd(args, client, json_output=True)

    assert len(output) == 2


def test_keypair_add_in_region():
    client = make_client(return_value=answers.KEYPAIR_ADD)

    args = ["keypair add",
            "--user", "88ad5569d8c64f828ac3d2efa4e552dd",
            "--name", "MOSCOW_KEY",
            "--key", "ssh-rsa ssh-rsa ... user@name",
            "--region", "ru-1",
            "--region", "ru-2"]

    output = run_cmd(args, client, json_output=True)

    assert len(output) == 2


def test_keypair_delete_without_accept():
    client = make_client(return_value=None)
    args = ["keypair delete", "MOSCOW_KEY",
            "--user", "88ad5569d8c64f828ac3d2efa4e552dd"]

    with pytest.raises(SystemExit):
        run_cmd(args, client)
