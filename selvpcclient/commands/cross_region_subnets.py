from selvpcclient.base import CLICommand, ListCommand
from selvpcclient.formatters import format_servers
from selvpcclient.util import (add_resource_filter_arguments, confirm_action,
                               handle_http_error)


class Add(ListCommand):
    """Add new cross-region subnet into project"""

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
            '--cidr',
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
            "cross_region_subnets": [
                {
                    "regions": [],
                    "quantity": parsed_args.quantity,
                },
            ],
        }
        for i in body["cross_region_subnets"]:
            for region in parsed_args.regions:
                i["regions"].append({"region": region})
            if parsed_args.cidr:
                i["cidr"] = parsed_args.cidr
        result = self.app.context["client"].cross_region_subnets.add(
            parsed_args.project_id, body
        )
        return self.setup_columns(result, parsed_args)


class Show(ListCommand):
    """Show detailed cross-region subnet information"""

    columns = [
        'id', 'project_id', 'cidr', 'status', 'servers'
    ]
    _formatters = {"servers": format_servers}

    def get_parser(self, prog_name):
        parser = super(ListCommand, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar="<cross_region_subnet_id>"
        )
        return parser

    @handle_http_error
    def take_action(self, parsed_args):
        result = self.app.context["client"].cross_region_subnets.show(
            parsed_args.id)
        return self.setup_columns([result._info], parsed_args)


class Delete(CLICommand):
    """Delete cross-region subnet from project"""

    def get_parser(self, prog_name):
        parser = super(CLICommand, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar="<cross_region_subnet_id>",
            nargs='+'
        )
        parser.add_argument(
            '--yes-i-really-want-to-delete',
            default=False,
            action='store_true'
        )
        return parser

    @confirm_action("delete")
    def take_action(self, parsed_args):
        self.app.context["client"].cross_region_subnets.delete_many(
            parsed_args.id,
            raise_if_not_found=False
        )


class List(ListCommand):
    """List of cross-region subnets"""

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

        result = self.app.context["client"].cross_region_subnets.list(
            project_id=parsed_args.project_id,
            detailed=parsed_args.detailed,
        )
        return self.setup_columns(result, parsed_args)
