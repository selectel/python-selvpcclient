#!/usr/bin/env python

import logging
import os
import os.path
import sys

from cliff.app import App
from cliff.commandmanager import CommandManager

from selvpcclient import __version__
from selvpcclient.client import Client
from selvpcclient.client import setup_http_client
from selvpcclient.commands import commands
from selvpcclient.httpclient import RegionalHTTPClient
from selvpcclient.util import parse_headers

logger = logging.getLogger(__name__)


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
            default=os.environ.get('SEL_URL', None)
        )
        parser.add_argument(
            '--identity_url',
            default=os.environ.get(
                'OS_AUTH_URL',
                'https://api.selvpc.ru/identity/v3'
            )
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
        parser.add_argument(
            '--http-timeout',
            dest='timeout',
            default=60,
            type=float,
            metavar='<seconds>',
            help='Timeout in seconds to wait for an HTTP response. '
                 'Default is 60 seconds'
        )
        return parser

    def configure_logging(self):
        if self.options.debug:
            self.options.verbose_level = 2
        super(CLI, self).configure_logging()

    def prepare_to_run_command(self, cmd):
        # NOTE: cliff earlier 2.8 doesn't fill "internal" commands.
        if not cmd.cmd_name or cmd.cmd_name in ['complete', 'help']:
            return

        if not self.options.url:
            logger.error("argument --url is required")
            sys.exit(1)

        headers = None
        if self.options.header:
            headers = parse_headers(self.options.header)

        http_client = setup_http_client(
            api_url=self.options.url,
            api_version=self.options.api_version,
            api_token=self.options.token,
            custom_headers=headers,
            timeout=self.options.timeout,
        )
        regional_http_client = RegionalHTTPClient(
            http_client=http_client,
            identity_url=self.options.identity_url
        )

        self.context = {
            'client': Client(
                client=http_client,
                regional_client=regional_http_client
            )
        }


def main(argv=sys.argv[1:]):
    shell = CLI()
    return shell.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
