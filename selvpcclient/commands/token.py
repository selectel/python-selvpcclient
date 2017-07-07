from selvpcclient.base import ShowCommand
from selvpcclient.util import handle_http_error


class Add(ShowCommand):
    """Create new token"""

    columns = ['id']

    def get_parser(self, prog_name):
        parser = super(ShowCommand, self).get_parser(prog_name)
        parser.add_argument(
            'project_id',
            metavar="<project_id>"
        )
        return parser

    @handle_http_error
    def take_action(self, parsed_args):
        result = self.app.context["client"].tokens.create(
            parsed_args.project_id
        )
        return self.setup_columns(result, parsed_args)
