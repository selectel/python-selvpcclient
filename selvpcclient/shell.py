#!/usr/bin/env python

import os
import os.path
import sys

from cliff.app import App
from cliff.commandmanager import CommandManager

from selvpcclient import __version__
from selvpcclient.client import Client, setup_http_client
from selvpcclient.commands import commands
from selvpcclient.util import parse_headers


class CLI(App):
    def __init__(self):
        super(CLI, self).__init__(
            description='Friendly Console Interface for the Selectel VPC.',
            version=__version__,
            command_manager=CommandManager('selvpc.commands'),
            deferred_help=False, )
        self.commands = commands
        for k, v in self.commands.items():
            self.command_manager.add_command(k, v)

    def build_option_parser(self, description, version, argparse_kwargs=None):
        parser = super(CLI, self).build_option_parser(description, version,
                                                      argparse_kwargs)
        parser.add_argument(
            '--url',
            required="SEL_URL" not in os.environ,
            default=os.environ.get('SEL_URL', None)
        )
        parser.add_argument(
            '--token',
            default=os.environ.get('SEL_TOKEN', None)
        )
        parser.add_argument(
            '--api-version',
            default=os.environ.get('SEL_API_VERSION', 2)
        )
        parser.add_argument(
            '-H',
            '--header',
            action='append'
        )
        return parser

    def configure_logging(self):
        if self.options.debug:
            self.options.verbose_level = 2
        super(CLI, self).configure_logging()

    def prepare_to_run_command(self, cmd):
        headers = None
        if self.options.header:
            headers = parse_headers(self.options.header)

        http_client = setup_http_client(
            api_url=self.options.url,
            api_version=self.options.api_version,
            api_token=self.options.token,
            custom_headers=headers
        )
        self.context = dict(client=Client(client=http_client))


def main(argv=sys.argv[1:]):
    shell = CLI()
    return shell.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
