from selvpcclient.base import ShowCommand, CLICommand
from selvpcclient.util import confirm_action, handle_http_error


class Create(ShowCommand):
    """Create new token. Provide account name for account-scoped token
    or project id for project-scoped."""

    columns = ['id']

    def get_parser(self, prog_name):
        parser = super(ShowCommand, self).get_parser(prog_name)
        required = parser.add_argument_group('Required arguments')
        required.add_argument('--project',
                              dest='project_id',
                              )
        required.add_argument('--account',
                              dest='account_name',
                              )
        return parser

    @handle_http_error
    def take_action(self, parsed_args):
        result = self.app.context["client"].tokens.create(
            parsed_args.project_id,
            parsed_args.account_name
        )
        return self.setup_columns(result, parsed_args)


class Delete(CLICommand):
    """Revoke user token"""

    def get_parser(self, prog_name):
        parser = super(CLICommand, self).get_parser(prog_name)
        required = parser.add_argument_group('Required arguments')
        required.add_argument('id',
                              metavar='<token_id>',
                              nargs='+',
                              )
        required.add_argument('--yes-i-really-want-to-delete',
                              default=False,
                              action='store_true',
                              )
        return parser

    @confirm_action("delete")
    def take_action(self, parsed_args):
        self.app.context["client"].tokens.delete_many(
            parsed_args.id,
            raise_if_not_found=False
        )
