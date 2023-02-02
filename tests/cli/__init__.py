import json

import mock
from selvpcclient.client import Client
from selvpcclient.shell import CLI


def prepare_to_run_command(cmd):
    pass


class FakeStdout(object):
    def __init__(self):
        self.content = []

    def write(self, text):
        self.content.append(text)

    def make_string(self):
        pass


def run_cmd(args, client, json_output=False, print_output=True):
    if json_output:
        args.extend(['-f', 'json'])
    stdout = FakeStdout()

    shell = CLI()
    shell.prepare_to_run_command = prepare_to_run_command
    shell.stdout = stdout
    shell.context = dict(client=client)
    shell.run(args)

    result = "".join(stdout.content)
    if print_output:
        print(result)
    if json_output:
        return json.loads(result)
    return result


def make_client(return_value):
    response = mock.Mock()
    response.json = mock.Mock(return_value=return_value)
    http_client = mock.Mock()
    methods = {
        "get.return_value": response,
        "post.return_value": response,
        "patch.return_value": response,
        "put.return_value": response,
        "delete.return_value": response,
    }
    http_client.configure_mock(**methods)
    return Client(client=http_client, regional_client=http_client)
