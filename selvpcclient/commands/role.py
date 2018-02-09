from selvpcclient.base import CLICommand, ListCommand, ShowCommand
from selvpcclient.util import confirm_action, handle_http_error


class Create(ShowCommand):
    """Create new role"""

    columns = ['project_id', 'user_id']
    sorting_support = True

    def get_parser(self, prog_name):
        parser = super(ShowCommand, self).get_parser(prog_name)
        parser.add_argument(
            '-p',
            '--project',
            required=True,
        )
        parser.add_argument(
            '-u',
            '--user',
            required=True,
        )
        return parser

    @handle_http_error
    def take_action(self, parsed_args):
        result = self.app.context["client"].roles.add_user_role_in_project(
            parsed_args.project, parsed_args.user
        )
        return self.setup_columns(result, parsed_args)


class Delete(CLICommand):
    """Delete role"""

    def get_parser(self, prog_name):
        parser = super(CLICommand, self).get_parser(prog_name)
        parser.add_argument(
            '-p',
            '--project',
            required=True,
        )
        parser.add_argument(
            '-u',
            '--user',
            required=True,
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
        self.app.context["client"].roles.delete_user_role_from_project(
            parsed_args.project, parsed_args.user
        )
        self.logger.info("User %s has been deleted from %s",
                         parsed_args.user, parsed_args.project)


class List(ListCommand):
    """List roles"""

    columns = ['project_id', 'user_id']
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
        result = self.app.context["client"].roles.get_project_roles(
            parsed_args.project_id
        )
        return self.setup_columns(result, parsed_args)
