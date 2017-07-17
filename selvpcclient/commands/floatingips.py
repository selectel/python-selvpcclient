from selvpcclient.base import CLICommand, ListCommand
from selvpcclient.formatters import format_servers
from selvpcclient.util import (add_resource_filter_arguments, confirm_action,
                               handle_http_error)


class Add(ListCommand):
    """Add new floatingip IP address"""

    columns = ['id', 'project_id', 'region', 'floating_ip_address', 'status']
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
        )
        parser.add_argument(
            '--quantity',
            required=False,
            default=1,
            type=int,
        )
        return parser

    @handle_http_error
    def take_action(self, parsed_args):
        body = {
            "floatingips": [{
                "region": parsed_args.region,
                "quantity": parsed_args.quantity,
            }]
        }
        result = self.app.context["client"].floatingips.add(
            parsed_args.project_id, body
        )
        return self.setup_columns(result, parsed_args)


class Show(ListCommand):
    """Show detailed floatingip information"""

    columns = [
        'id', 'project_id', 'region', 'floating_ip_address', 'status',
        'servers'
    ]
    _formatters = {"servers": format_servers}

    def get_parser(self, prog_name):
        parser = super(ListCommand, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar="<floating_ip_id>"
        )
        return parser

    @handle_http_error
    def take_action(self, parsed_args):
        result = self.app.context["client"].floatingips.show(parsed_args.id)
        return self.setup_columns([result._info], parsed_args)


class Delete(CLICommand):
    """Delete floatingip IP"""

    def get_parser(self, prog_name):
        parser = super(CLICommand, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar="<floating_ip_id>"
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
        self.app.context["client"].floatingips.delete(parsed_args.id)
        self.logger.info("IP {} was deleted".format(parsed_args.id))


class List(ListCommand):
    """List floatingip IP"""

    columns = ['id', 'project_id', 'region', 'floating_ip_address', 'status']
    sorting_support = True

    def get_parser(self, prog_name):
        parser = super(ListCommand, self).get_parser(prog_name)
        parser.add_argument(
            '--detailed',
            default=False,
            action='store_true'
        )
        add_resource_filter_arguments(parser)
        return parser

    @handle_http_error
    def take_action(self, parsed_args):
        if parsed_args.detailed:
            self.columns.append('servers')
            self._formatters = {"servers": format_servers}

        result = self.app.context["client"].floatingips.list(
            detailed=parsed_args.detailed,
            project_id=parsed_args.project_id,
            region=parsed_args.region,
        )
        return self.setup_columns(result, parsed_args)
