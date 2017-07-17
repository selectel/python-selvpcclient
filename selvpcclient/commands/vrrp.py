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
        parser.add_argument(
            'project_id',
            metavar="<project_id>"
        )
        parser.add_argument(
            '-r',
            '--region',
            required=True,
            action='append',
            dest="regions",
        )
        parser.add_argument(
            '--type',
            default="ipv4",
        )
        parser.add_argument(
            '-p',
            '--prefix',
            default=29,
            type=int,
        )
        parser.add_argument(
            '--quantity',
            default=1,
            type=int,
        )
        return parser

    @handle_http_error
    def take_action(self, parsed_args):
        body = {
            "vrrp_subnets": [
                {
                    "regions": parsed_args.regions,
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

    columns = [
        'id', 'project_id', 'cidr', 'status', 'servers'
    ]
    _formatters = {"servers": format_servers}

    def get_parser(self, prog_name):
        parser = super(ListCommand, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar="<vrrp_id>"
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
        parser.add_argument(
            'id',
            metavar="<vrrp_id>",
            nargs='+'
        )
        parser.add_argument(
            '--yes-i-really-want-to-delete',
            default=False,
            action='store_true'
        )
        return parser

    @handle_http_error
    @confirm_action("delete")
    def take_action(self, parsed_args):
        if len(parsed_args.id) > 1:
            self.app.context["client"].vrrp.delete_many(
                parsed_args.id,
                raise_if_not_found=False
            )
        else:
            self.app.context["client"].vrrp.delete(parsed_args.id[0])


class List(ListCommand):
    """List of vrrp subnets"""

    columns = ['id', 'project_id', 'cidr', 'status']
    sorting_support = True

    def get_parser(self, prog_name):
        parser = super(ListCommand, self).get_parser(prog_name)
        parser.add_argument(
            '--detailed',
            default=False,
            action='store_true'
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
