from selvpcclient.base import ListCommand
from selvpcclient.exceptions.base import ClientException
from selvpcclient.formatters import join_by_key
from selvpcclient.formatters import reformat_quotas
from selvpcclient.formatters import reformat_quotas_with_usages
from selvpcclient.util import extract_single_quota_error, handle_http_error


class Update(ListCommand):
    """Set quotas for project"""

    columns = ['resource', 'zone', 'value']
    _formatters = {
        "zone": join_by_key("zone"),
        "value": join_by_key("value"),
        "used": join_by_key("used")
    }
    sorting_support = True

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
        required.add_argument('-R',
                              '--resource',
                              required=True,
                              )
        required.add_argument('--value',
                              required=True,
                              type=int,
                              )

        optional = parser.add_argument_group('Optional arguments')
        optional.add_argument('-z',
                              '--zone',
                              required=False,
                              default=None,
                              )
        return parser

    @handle_http_error
    def take_action(self, parsed_args):
        quotas = {
            'quotas': {
                parsed_args.resource: [{
                    "zone": parsed_args.zone,
                    "value": parsed_args.value
                }]
            }
        }
        try:
            result = self.app.context["client"].quotas.update_project_quotas(
                project_id=parsed_args.project_id,
                region=parsed_args.region,
                quotas=quotas,
            )
        except ClientException as e:
            # Through the CLI, you can set a quota for only 1 resource.
            # It is assumed that there will be only one error.
            raise Exception(extract_single_quota_error(e))

        return self.setup_columns(
            reformat_quotas(result._info), parsed_args
        )


class Show(ListCommand):
    """Show quotas for project"""

    columns = ['resource', 'zone', 'value', 'used']
    _formatters = {
        "zone": join_by_key("zone"),
        "value": join_by_key("value"),
        "used": join_by_key("used")
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
        result = self.app.context["client"].quotas.get_project_quotas(
            project_id=parsed_args.project_id,
            region=parsed_args.region
        )

        return self.setup_columns(
            reformat_quotas_with_usages(result._info), parsed_args
        )
