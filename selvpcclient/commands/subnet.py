from selvpcclient.base import CLICommand, ListCommand, ShowCommand
from selvpcclient.formatters import format_servers
from selvpcclient.util import (confirm_action,
                               handle_http_error,
                               add_resource_filter_arguments)


class Add(ListCommand):
    """Add new subnet"""

    columns = ['id', 'project_id', 'region', 'cidr', 'status']

    def get_parser(self, prog_name):
        parser = super(ListCommand, self).get_parser(prog_name)
        required = parser.add_argument_group('Required arguments')
        required.add_argument('project_id',
                              metavar='<project_id>',
                              )
        required.add_argument('-r',
                              '--region',
                              required=True,
                              )
        required.add_argument('-t',
                              '--type',
                              required=True,
                              )
        optional = parser.add_argument_group('Optional arguments')
        optional.add_argument('-p',
                              '--prefix',
                              default=29,
                              type=int,
                              )
        optional.add_argument('--quantity',
                              default=1,
                              type=int,
                              )
        return parser

    @handle_http_error
    def take_action(self, parsed_args):
        subnets = {
            "subnets": [{
                "region": parsed_args.region,
                "quantity": parsed_args.quantity,
                "type": parsed_args.type,
                "prefix_length": parsed_args.prefix
            }]
        }
        result = self.app.context["client"].subnets.add(
            parsed_args.project_id, subnets
        )
        return self.setup_columns(result, parsed_args)


class Show(ShowCommand):
    """Show detailed subnet information"""

    columns = [
        'id', 'project_id', 'network_id', 'region', 'cidr', 'status', 'servers'
    ]

    def get_parser(self, prog_name):
        parser = super(ShowCommand, self).get_parser(prog_name)
        required = parser.add_argument_group('Required arguments')
        required.add_argument('id',
                              metavar='<subnet_id>',
                              )
        return parser

    @handle_http_error
    def take_action(self, parsed_args):
        result = self.app.context["client"].subnets.show(parsed_args.id)
        return self.setup_columns(result, parsed_args)


class Delete(CLICommand):
    """Delete subnet"""

    def get_parser(self, prog_name):
        parser = super(CLICommand, self).get_parser(prog_name)
        required = parser.add_argument_group('Required arguments')
        required.add_argument('id',
                              metavar='<subnet_id>',
                              nargs='+',
                              )
        required.add_argument('--yes-i-really-want-to-delete',
                              default=False,
                              action='store_true',
                              )
        return parser

    @confirm_action("delete")
    def take_action(self, parsed_args):
        self.app.context["client"].subnets.delete_many(
            parsed_args.id,
            raise_if_not_found=False
        )


class List(ListCommand):
    """List subnets"""

    columns = ['id', 'project_id', 'region', 'cidr', 'status']
    sorting_support = True

    def get_parser(self, prog_name):
        parser = super(ListCommand, self).get_parser(prog_name)
        optional = parser.add_argument_group('Optional arguments')
        optional.add_argument('--detailed',
                              default=False,
                              action='store_true',
                              )
        add_resource_filter_arguments(parser)
        return parser

    @handle_http_error
    def take_action(self, parsed_args):
        if parsed_args.detailed:
            self.columns.append('servers')
            self._formatters = {"servers": format_servers}

        result = self.app.context["client"].subnets.list(
            detailed=parsed_args.detailed,
            project_id=parsed_args.project_id,
            region=parsed_args.region,
        )
        return self.setup_columns(result, parsed_args)
