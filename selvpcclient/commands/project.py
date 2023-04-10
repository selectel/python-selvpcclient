from selvpcclient.base import CLICommand, ListCommand, ShowCommand
from selvpcclient.util import (confirm_action, handle_http_error,
                               convert_to_short)


class Create(ShowCommand):
    """Create new project"""

    columns = ["id", "name", "url", "enabled"]

    def get_parser(self, prog_name):
        parser = super(ShowCommand, self).get_parser(prog_name)
        required = parser.add_argument_group('Required arguments')
        required.add_argument('-n',
                              '--name',
                              required=True,
                              )
        required.add_argument('--skip_quotas_init',
                              default=False,
                              action='store_true'
                              )
        return parser

    @handle_http_error
    def take_action(self, parsed_args):
        result = self.app.context["client"].projects.create(
            parsed_args.name, parsed_args.skip_quotas_init)
        return self.setup_columns(result, parsed_args)


class Update(ShowCommand):
    """Set project properties"""

    columns = ["id", "name", "url", "custom_url",
               "enabled", "color", "logo", "brand_color"]

    def get_parser(self, prog_name):
        parser = super(ShowCommand, self).get_parser(prog_name)
        required = parser.add_argument_group('Required arguments')
        required.add_argument('id',
                              metavar='<project_id>',
                              )

        optional = parser.add_argument_group('Optional arguments')
        optional.add_argument('-n',
                              '--name',
                              metavar='NEW_NAME',
                              )
        optional.add_argument('--cname',
                              )
        optional.add_argument('--color',
                              )
        optional.add_argument('--logo',
                              )
        optional.add_argument('--brand-color',
                              )
        optional.add_argument('--reset-cname',
                              default=False,
                              action='store_true',
                              )
        optional.add_argument('--reset-color',
                              default=False,
                              action='store_true',
                              )
        optional.add_argument('--reset-logo',
                              default=False,
                              action='store_true',
                              )
        optional.add_argument('--reset-theme',
                              default=False,
                              action='store_true',
                              )
        optional.add_argument('--reset-brand-color',
                              default=False,
                              action='store_true',
                              )
        optional.add_argument('--show-base64',
                              default=False,
                              action='store_true',
                              )
        optional.add_argument('--show-short-base64',
                              default=False,
                              action='store_true',
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
            brand_color=parsed_args.brand_color,
            reset_cname=parsed_args.reset_cname,
            reset_color=parsed_args.reset_color,
            reset_logo=parsed_args.reset_logo,
            reset_theme=parsed_args.reset_theme,
            reset_brand_color=parsed_args.reset_brand_color,
        )
        result.logo = result["theme"]["logo"]
        result.color = result["theme"]["color"]
        result.brand_color = result["theme"]["brand_color"]

        if parsed_args.show_short_base64:
            result.logo = convert_to_short(result.logo)
        elif not parsed_args.show_base64:
            result.logo = result.logo != ""
        return self.setup_columns(result, parsed_args)


class Show(ShowCommand):
    """Display project info"""

    columns = ["id", "name", "url", "custom_url",
               "enabled", "color", "logo", "brand_color"]

    def get_parser(self, prog_name):
        parser = super(ShowCommand, self).get_parser(prog_name)
        required = parser.add_argument_group('Required arguments')
        required.add_argument('id',
                              metavar='<project_id>',
                              )

        optional = parser.add_argument_group('Optional arguments')
        optional.add_argument('--show-base64',
                              default=False,
                              action='store_true',
                              )
        optional.add_argument('--show-short-base64',
                              default=False,
                              action='store_true',
                              )
        return parser

    @handle_http_error
    def take_action(self, parsed_args):
        result = self.app.context["client"].projects.show(parsed_args.id)
        result.logo = result["theme"]["logo"]
        result.color = result["theme"]["color"]
        result.brand_color = result["theme"]["brand_color"]

        if parsed_args.show_short_base64:
            result.logo = convert_to_short(result.logo)
        elif not parsed_args.show_base64:
            result.logo = result.logo != ""
        return self.setup_columns(result, parsed_args)


class Delete(CLICommand):
    """Delete project"""

    def get_parser(self, prog_name):
        parser = super(CLICommand, self).get_parser(prog_name)
        required = parser.add_argument_group('Required arguments')
        required.add_argument('id',
                              metavar='<project_id>',
                              nargs='+',
                              )
        required.add_argument('--yes-i-really-want-to-delete',
                              action='store_true',
                              )
        return parser

    @confirm_action("delete")
    def take_action(self, parsed_args):
        self.app.context["client"].projects.delete_many(
            parsed_args.id,
            raise_if_not_found=False
        )


class List(ListCommand):
    """List projects"""

    columns = ["id", "name", "url", "enabled"]
    sorting_support = True

    @handle_http_error
    def take_action(self, parsed_args):
        result = self.app.context["client"].projects.list()
        return self.setup_columns(result, parsed_args)
