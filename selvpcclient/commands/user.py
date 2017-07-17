from selvpcclient.base import CLICommand, ListCommand, ShowCommand
from selvpcclient.util import confirm_action, handle_http_error


class Create(ShowCommand):
    """Create new user"""

    columns = ['id', 'name', 'enabled']

    def get_parser(self, prog_name):
        parser = super(ShowCommand, self).get_parser(prog_name)
        parser.add_argument(
            '--name',
            required=True,
        )
        parser.add_argument(
            '--password',
            required=True,
        )
        parser.add_argument(
            '--enabled',
            default=True
        )
        return parser

    @handle_http_error
    def take_action(self, parsed_args):
        result = self.app.context["client"].users.create(
            parsed_args.name, parsed_args.password, parsed_args.enabled
        )
        return self.setup_columns(result, parsed_args)


class Update(ShowCommand):
    """Update user properties"""

    columns = ['id', 'name', 'enabled']

    def get_parser(self, prog_name):
        parser = super(ShowCommand, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar="<user_id>"
        )
        parser.add_argument(
            '--name',
        )
        parser.add_argument(
            '--password',
        )
        parser.add_argument(
            '--enabled',
        )
        return parser

    @handle_http_error
    def take_action(self, parsed_args):
        result = self.app.context["client"].users.update(
            parsed_args.id, parsed_args.name, parsed_args.password,
            parsed_args.enabled
        )
        return self.setup_columns(result, parsed_args)


class Delete(CLICommand):
    """Delete user"""

    def get_parser(self, prog_name):
        parser = super(CLICommand, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar="<user_id>",
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
            self.app.context["client"].users.delete_many(
                parsed_args.id,
                raise_if_not_found=False
            )
        else:
            self.app.context["client"].users.delete(parsed_args.id[0])


class List(ListCommand):
    """List users"""

    columns = ['id', 'name', 'enabled']
    sorting_support = True

    @handle_http_error
    def take_action(self, parsed_args):
        result = self.app.context["client"].users.list()
        return self.setup_columns(result, parsed_args)


class RolesList(ListCommand):
    """List user-role assignments"""

    columns = ['project_id', 'user_id']
    sorting_support = True

    def get_parser(self, prog_name):
        parser = super(ListCommand, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar="<user_id>"
        )
        return parser

    @handle_http_error
    def take_action(self, parsed_args):
        result = self.app.context["client"].roles.get_user_roles(
            parsed_args.id
        )
        return self.setup_columns(result, parsed_args)
