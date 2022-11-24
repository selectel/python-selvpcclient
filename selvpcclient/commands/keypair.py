from selvpcclient.base import CLICommand, ListCommand
from selvpcclient.util import (add_resource_filter_arguments, confirm_action,
                               handle_http_error)


class Add(ListCommand):
    """Add keypair to all regions"""

    columns = ['region', 'user_id', 'name']
    sorting_support = True

    def get_parser(self, prog_name):
        parser = super(ListCommand, self).get_parser(prog_name)
        required = parser.add_argument_group('Required arguments')
        required.add_argument('--key',
                              metavar='ID_RSA_KEY',
                              dest='public_key',
                              )
        required.add_argument('--user',
                              required=True,
                              metavar='USER_ID',
                              dest='user_id',
                              )
        required.add_argument('--name',
                              required=True,
                              metavar='KEY_NAME',
                              )
        required.add_argument('--region',
                              metavar='REGION',
                              dest='regions',
                              action='append',
                              )
        return parser

    @handle_http_error
    def take_action(self, parsed_args):
        body = {
            "keypair": {
                "user_id": parsed_args.user_id,
                "public_key": parsed_args.public_key,
                "name": parsed_args.name,
            }
        }
        if parsed_args.regions:
            body["keypair"]["regions"] = parsed_args.regions
        result = self.app.context["client"].keypairs.add(keypair=body)
        return self.setup_columns(result, parsed_args)


class Delete(CLICommand):
    """Delete keypairs for specific user"""

    def get_parser(self, prog_name):
        parser = super(CLICommand, self).get_parser(prog_name)
        required = parser.add_argument_group('Required arguments')
        required.add_argument('-u',
                              '--user',
                              metavar='USER_ID',
                              dest='user_id',
                              )
        required.add_argument('keys',
                              metavar='<key_name>',
                              nargs='+',
                              )
        required.add_argument('--yes-i-really-want-to-delete',
                              default=False,
                              action='store_true',
                              )
        return parser

    @confirm_action("delete")
    def take_action(self, parsed_args):
        self.app.context["client"].keypairs.delete_many(
            user_id=parsed_args.user_id,
            key_names=parsed_args.keys,
            raise_if_not_found=False
        )


class List(ListCommand):
    """List of keypairs in all regions"""
    sorting_support = True
    columns = ['name', 'user_id', 'regions']
    _formatters = {
        "regions": lambda line: "\n".join(line["regions"])
    }

    def get_parser(self, prog_name):
        parser = super(ListCommand, self).get_parser(prog_name)
        add_resource_filter_arguments(parser, add_project=False)
        optional = parser.add_argument_group('Optional arguments')
        optional.add_argument('--show-key',
                              default=False,
                              action='store_true',
                              )
        optional.add_argument('--show-short-key',
                              default=False,
                              action='store_true',
                              )
        optional.add_argument('-u',
                              '--user',
                              metavar='USER_ID',
                              dest='user_id',
                              required=False,
                              default=None,
                              )
        return parser

    @handle_http_error
    def take_action(self, parsed_args):
        result = self.app.context["client"].keypairs.list(
            user_id=parsed_args.user_id
        )
        if parsed_args.show_key or parsed_args.show_short_key:
            self.columns.append("public_key")
        if parsed_args.show_short_key and not parsed_args.show_key:
            self._formatters["public_key"] = \
                lambda line: '...' + line["public_key"][-30:]
        return self.setup_columns(result, parsed_args)
