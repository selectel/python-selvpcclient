from selvpcclient.base import ShowCommand
from selvpcclient.util import handle_http_error


class Create(ShowCommand):
    """Create new token. Provide domain name for domain-scoped token
    or project id for project-scoped."""

    columns = ['id']

    def get_parser(self, prog_name):
        parser = super(ShowCommand, self).get_parser(prog_name)
        parser.add_argument(
            '--project',
            dest='project_id'
        )
        parser.add_argument(
            '--domain',
            dest='domain_name',
        )
        return parser

    @handle_http_error
    def take_action(self, parsed_args):
        result = self.app.context["client"].tokens.create(
            parsed_args.project_id,
            parsed_args.domain_name
        )
        return self.setup_columns(result, parsed_args)
