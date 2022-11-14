from selvpcclient.base import ListCommand
from selvpcclient.formatters import join_by_key, reformat_limits
from selvpcclient.util import handle_http_error


class Show(ListCommand):
    """Show project limits"""

    columns = ["resource", "zone", "value"]
    _formatters = {
        "zone": join_by_key("zone"),
        "value": join_by_key("value")
    }
    sorting_support = True

    def get_parser(self, prog_name):
        parser = super(ListCommand, self).get_parser(prog_name)
        required = parser.add_argument_group('Required arguments')
        required.add_argument('-r',
                              '--region',
                              required=True,
                              )
        required.add_argument('project_id',
                              metavar='<project_id>',
                              )
        return parser

    @handle_http_error
    def take_action(self, parsed_args):
        result = self.app.context["client"].quotas.get_project_limits(
            project_id=parsed_args.project_id,
            region=parsed_args.region
        )

        return self.setup_columns(
            reformat_limits(result._info), parsed_args
        )
