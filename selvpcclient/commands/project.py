from selvpcclient.base import CLICommand, ListCommand, ShowCommand
from selvpcclient.util import (confirm_action, get_item_properties,
                               handle_http_error, convert_to_short)


class Create(ShowCommand):
    """Create new project"""

    columns = ["id", "name", "url", "enabled"]

    def get_parser(self, prog_name):
        parser = super(ShowCommand, self).get_parser(prog_name)
        parser.add_argument(
            '-n',
            '--name',
            required=True,
        )
        return parser

    @handle_http_error
    def take_action(self, parsed_args):
        result = self.app.context["client"].projects.create(parsed_args.name)
        return self.setup_columns(result, parsed_args)


class Update(ShowCommand):
    """Set project properties"""

    columns = ["id", "name", "url", "custom_url",
               "enabled", "color", "logo"]

    def get_parser(self, prog_name):
        parser = super(ShowCommand, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar="<project_id>"
        )
        parser.add_argument(
            '-n',
            '--name',
            metavar="NEW_NAME"
        )
        parser.add_argument('--cname')
        parser.add_argument('--color')
        parser.add_argument('--logo')
        parser.add_argument(
            '--reset-cname',
            default=False,
            action="store_true"
        )
        parser.add_argument(
            '--reset-color',
            default=False,
            action="store_true"
        )
        parser.add_argument(
            '--reset-logo',
            default=False,
            action="store_true"
        )
        parser.add_argument(
            '--reset-theme',
            default=False,
            action="store_true"
        )
        parser.add_argument(
            '--show-base64',
            default=False,
            action='store_true'
        )
        parser.add_argument(
            '--show-short-base64',
            default=False,
            action='store_true'
        )
        return parser

    @handle_http_error
    def take_action(self, parsed_args):
        result = self.app.context["client"].projects.update(
            parsed_args.id,
            parsed_args.name,
            cname=parsed_args.cname,
            color=parsed_args.color,
            logo=parsed_args.logo,
            reset_cname=parsed_args.reset_cname,
            reset_color=parsed_args.reset_color,
            reset_logo=parsed_args.reset_logo,
            reset_theme=parsed_args.reset_theme
        )
        result.logo = result["theme"]["logo"]
        result.color = result["theme"]["color"]

        if parsed_args.show_short_base64:
            result.logo = convert_to_short(result.logo)
        elif not parsed_args.show_base64:
            result.logo = result.logo != ""
        return self.setup_columns(result, parsed_args)


class Show(ShowCommand):
    """Display project info"""

    columns = ["id", "name", "url", "custom_url",
               "enabled", "color", "logo"]

    def get_parser(self, prog_name):
        parser = super(ShowCommand, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar="<project_id>"
        )
        parser.add_argument(
            '--show-base64',
            default=False,
            action='store_true'
        )
        parser.add_argument(
            '--show-short-base64',
            default=False,
            action='store_true'
        )
        return parser

    @handle_http_error
    def take_action(self, parsed_args):
        result = self.app.context["client"].projects.show(parsed_args.id)
        result.logo = result["theme"]["logo"]
        result.color = result["theme"]["color"]

        if parsed_args.show_short_base64:
            result.logo = convert_to_short(result.logo)
        elif not parsed_args.show_base64:
            result.logo = result.logo != ""
        return self.setup_columns(result, parsed_args)


class Delete(CLICommand):
    """Delete project"""

    def get_parser(self, prog_name):
        parser = super(CLICommand, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar="<project_id>"
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
        self.app.context["client"].projects.delete(parsed_args.id)
        self.logger.info("Project {} was deleted".format(parsed_args.id))


class List(ListCommand):
    """List projects"""

    columns = ["id", "name", "url", "enabled"]
    sorting_support = True

    @handle_http_error
    def take_action(self, parsed_args):
        result = self.app.context["client"].projects.list()
        return self.setup_columns(result, parsed_args)
