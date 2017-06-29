from tests.cli import make_client, run_cmd
from tests.util import answers

COUNT_OF_LIMITS = 9


def test_limit_show():
    client = make_client(return_value=answers.LIMITS_SHOW)
    args = ['limit show']

    output = run_cmd(args, client, json_output=True)

    assert len(output) == COUNT_OF_LIMITS


def test_limit_show_free():
    client = make_client(return_value=answers.LIMITS_SHOW_FREE)
    args = ['limit show free']

    output = run_cmd(args, client, json_output=True)

    assert len(output) == COUNT_OF_LIMITS
