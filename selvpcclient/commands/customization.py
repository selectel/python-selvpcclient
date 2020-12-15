from selvpcclient.base import ShowCommand, CLICommand
from selvpcclient.util import (handle_http_error,
                               confirm_action, convert_to_short)


class Update(ShowCommand):
    """Set customization properties."""

    columns = ["color", "logo", "brand_color"]

    def get_parser(self, prog_name):
        parser = super(ShowCommand, self).get_parser(prog_name)
        optional = parser.add_argument_group('Optional arguments')
        optional.add_argument('--logo',
                              )
        optional.add_argument('--color',
                              )
        optional.add_argument('--brand-color',
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
        result = self.app.context["client"].customization.update(
            color=parsed_args.color,
            logo=parsed_args.logo,
            brand_color=parsed_args.brand_color)
        if parsed_args.show_short_base64:
            result.logo = convert_to_short(result.logo)
        elif not parsed_args.show_base64:
            result.logo = result.logo != ""
        return self.setup_columns(result, parsed_args)


class Show(ShowCommand):
    """Display customization info."""

    columns = ["color", "logo", "brand_color"]

    def get_parser(self, prog_name):
        parser = super(ShowCommand, self).get_parser(prog_name)
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
        result = self.app.context["client"].customization.show()
        if parsed_args.show_short_base64:
            result.logo = convert_to_short(result.logo)
        elif not parsed_args.show_base64:
            result.logo = result.logo != ""
        return self.setup_columns(result, parsed_args)


class Delete(CLICommand):
    """Delete customization."""

    def get_parser(self, prog_name):
        parser = super(CLICommand, self).get_parser(prog_name)
        required = parser.add_argument_group('Required arguments')
        required.add_argument('--yes-i-really-want-to-delete',
                              default=False,
                              action='store_true',
                              )
        return parser

    @handle_http_error
    @confirm_action("delete")
    def take_action(self, parsed_args):
        self.app.context["client"].customization.delete()
        self.logger.info("The theme has been deleted")
