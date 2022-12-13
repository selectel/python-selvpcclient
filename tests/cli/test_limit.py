from tests.cli import make_client, run_cmd
from tests.util import answers

COUNT_OF_LIMITS = 9


def test_limit_show():
    client = make_client(return_value=answers.LIMITS_SHOW)
    args = ['limit show', '--region=ru-1', 'c2383dc1894748b193031ae1bccf508a']

    output = run_cmd(args, client, json_output=True)

    assert len(output) == COUNT_OF_LIMITS
