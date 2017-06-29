from tests.cli import make_client, run_cmd
from tests.util import answers


def test_token_create():
    client = make_client(return_value=answers.TOKENS_CREATE)
    args = ['token create', 'project_id_here']

    output = run_cmd(args, client, json_output=True)

    assert 'id' in output
    assert 'a9a81014462d499d9d55d3402991f224' in output['id']
