from selvpcclient.base import CLICommand, ListCommand
from selvpcclient.formatters import format_servers
from selvpcclient.util import (add_resource_filter_arguments, confirm_action,
                               handle_http_error)


class Add(ListCommand):
    """Add new vrrp subnet into project"""

    columns = ['id', 'project_id', 'cidr', 'status']
    sorting_support = True

    def get_parser(self, prog_name):
        parser = super(ListCommand, self).get_parser(prog_name)
        required = parser.add_argument_group('Required arguments')
        required.add_argument('project_id',
                              metavar='<project_id>',
                              help='Project id'
                              )
        required.add_argument('-m',
                              '--master',
                              required=True,
                              action='store',
                              dest='master',
                              )
        required.add_argument('-s',
                              '--slave',
                              required=True,
                              action='store',
                              dest='slave',
                              )
        optional = parser.add_argument_group('Optional arguments')
        optional.add_argument('--type',
                              default='ipv4',
                              )
        optional.add_argument('-p',
                              '--prefix',
                              type=int,
                              default=29,
                              )
        optional.add_argument('--quantity',
                              type=int,
                              default=1,
                              )
        return parser

    @handle_http_error
    def take_action(self, parsed_args):
        body = {
            "vrrp_subnets": [
                {
                    "regions": {
                        "master": parsed_args.master,
                        "slave": parsed_args.slave
                    },
                    "prefix_length": parsed_args.prefix,
                    "type": parsed_args.type,
                    "quantity": parsed_args.quantity,
                }
            ]
        }
        result = self.app.context["client"].vrrp.add(
            parsed_args.project_id, body
        )
        return self.setup_columns(result, parsed_args)


class Show(ListCommand):
    """Show detailed vrrp subnet information"""

    columns = ['id', 'project_id', 'cidr', 'status', 'servers',
               'master_region', 'slave_region']
    _formatters = {"servers": format_servers}

    def get_parser(self, prog_name):
        parser = super(ListCommand, self).get_parser(prog_name)
        required = parser.add_argument_group('Required arguments')
        required.add_argument('id',
                              metavar='<vrrp_id>',
                              help='Project VRRP subnet id'
                              )
        return parser

    @handle_http_error
    def take_action(self, parsed_args):
        result = self.app.context["client"].vrrp.show(parsed_args.id)
        return self.setup_columns([result._info], parsed_args)


class Delete(CLICommand):
    """Delete vrrp subnet from project"""

    def get_parser(self, prog_name):
        parser = super(CLICommand, self).get_parser(prog_name)
        required = parser.add_argument_group('Required arguments')
        required.add_argument('id',
                              nargs='+',
                              metavar='<vrrp_id>',
                              help='Project VRRP subnet ids')
        required.add_argument('--yes-i-really-want-to-delete',
                              default=False,
                              action='store_true',
                              )
        return parser

    @confirm_action("delete")
    def take_action(self, parsed_args):
        self.app.context["client"].vrrp.delete_many(
            parsed_args.id,
            raise_if_not_found=False
        )


class List(ListCommand):
    """List of vrrp subnets"""

    columns = ['id', 'project_id', 'cidr', 'status', 'master_region',
               'slave_region']
    sorting_support = True

    def get_parser(self, prog_name):
        parser = super(ListCommand, self).get_parser(prog_name)
        optional = parser.add_argument_group('Optional arguments')
        optional.add_argument('--detailed',
                              default=False,
                              action='store_true',
                              )
        add_resource_filter_arguments(parser, add_region=False)
        return parser

    @handle_http_error
    def take_action(self, parsed_args):
        if parsed_args.detailed:
            self.columns.append('servers')
            self._formatters = {"servers": format_servers}

        result = self.app.context["client"].vrrp.list(
            project_id=parsed_args.project_id,
        )
        return self.setup_columns(result, parsed_args)
