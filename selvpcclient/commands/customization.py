from selvpcclient.base import ShowCommand, CLICommand
from selvpcclient.util import handle_http_error, confirm_action


class Update(ShowCommand):
    """Set customization properties."""

    columns = ["color", "logo"]

    def get_parser(self, prog_name):
        parser = super(ShowCommand, self).get_parser(prog_name)
        parser.add_argument('--logo')
        parser.add_argument('--color')
        return parser

    @handle_http_error
    def take_action(self, parsed_args):
        result = self.app.context["client"].customization.update(
            color=parsed_args.color,
            logo=parsed_args.logo)
        return self.setup_columns(result, parsed_args)


class Show(ShowCommand):
    """Display customization info."""

    columns = ["color", "logo"]

    @handle_http_error
    def take_action(self, parsed_args):
        result = self.app.context["client"].customization.show()
        return self.setup_columns(result, parsed_args)


class Delete(CLICommand):
    """Delete customization."""

    def get_parser(self, prog_name):
        parser = super(CLICommand, self).get_parser(prog_name)

        parser.add_argument(
            '--yes-i-really-want-to-delete',
            default=False,
            action='store_true'
        )
        return parser

    @handle_http_error
    @confirm_action("delete")
    def take_action(self, parsed_args):
        self.app.context["client"].customization.delete()
        self.logger.info("Theme was deleted")
