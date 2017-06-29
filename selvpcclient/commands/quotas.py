import sys

from selvpcclient.base import ListCommand, ParticleResponse
from selvpcclient.formatters import join_by_key, reformat_quotas_with_usages
from selvpcclient.util import handle_http_error


class List(ListCommand):
    """Show quotas for all projects"""

    columns = ['project_id', 'resource', 'region', 'zone', 'value', 'used']
    _formatters = {
        "region": join_by_key("region"),
        "zone": join_by_key("zone"),
        "value": join_by_key("value"),
        "used": join_by_key("used")
    }
    sorting_support = True

    @handle_http_error
    def take_action(self, parsed_args):
        result = self.app.context["client"].quotas.get_projects_quotas()
        return self.setup_columns(
            reformat_quotas_with_usages(result._info), parsed_args
        )


class Update(ListCommand):
    """Set quotas for project"""

    columns = ['resource', 'region', 'zone', 'value', 'used']
    _formatters = {
        "region": join_by_key("region"),
        "zone": join_by_key("zone"),
        "value": join_by_key("value"),
        "used": join_by_key("used")
    }
    sorting_support = True

    def get_parser(self, prog_name):
        parser = super(ListCommand, self).get_parser(prog_name)
        parser.add_argument(
            'project_id',
            metavar="<project_id>"
        )
        parser.add_argument(
            '-R',
            '--resource',
            required=True,
        )
        parser.add_argument(
            '-r',
            '--region',
            required=True,
        )
        parser.add_argument(
            '-z',
            '--zone',
            required=False,
            default=None,
        )
        parser.add_argument(
            '--value',
            required=True,
            type=int,
        )
        return parser

    @handle_http_error
    def take_action(self, parsed_args):
        quotas = {
            'quotas': {
                parsed_args.resource: [{
                    "region": parsed_args.region,
                    "zone": parsed_args.zone,
                    "value": parsed_args.value
                }]
            }
        }
        result = self.app.context["client"].quotas.update(
            parsed_args.project_id, quotas
        )
        if isinstance(result, ParticleResponse):
            result._info = result._info["quotas"]
        val = {parsed_args.project_id: result._info}
        return self.setup_columns(
            reformat_quotas_with_usages(val), parsed_args
        )


class Show(ListCommand):
    """Show quotas for project"""

    columns = ['resource', 'region', 'zone', 'value', 'used']
    _formatters = {
        "region": join_by_key("region"),
        "zone": join_by_key("zone"),
        "value": join_by_key("value"),
        "used": join_by_key("used")
    }
    sorting_support = True

    def get_parser(self, prog_name):
        parser = super(ListCommand, self).get_parser(prog_name)
        parser.add_argument(
            'project_id',
            metavar="<project_id>"
        )
        return parser

    @handle_http_error
    def take_action(self, parsed_args):
        result = self.app.context["client"].quotas.get_project_quotas(
            parsed_args.project_id
        )

        val = {parsed_args.project_id: result._info}
        return self.setup_columns(
            reformat_quotas_with_usages(val), parsed_args
        )


class Optimize(Show):
    """Optimize quotas for project"""

    @handle_http_error
    def take_action(self, parsed_args):
        result = self.app.context["client"].quotas.optimize_project_quotas(
            parsed_args.project_id
        )

        if not result:
            self.logger.warning("Nothing to optimize!")
            sys.exit(1)

        val = {parsed_args.project_id: result._info}
        return self.setup_columns(
            reformat_quotas_with_usages(val), parsed_args
        )
